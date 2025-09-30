import pytest
import time
from python_voltage_monitor.readers.impl.current_jump_strategy import CurrentJumpStrategy
from python_voltage_monitor.readers.impl.current_smooth_change_strategy import CurrentSmoothChangeStrategy, Direction
from python_voltage_monitor.readers.impl.plc_voltage_reader import PLCVoltageReader
from python_voltage_monitor.services.voltage_service import VoltageReaderService
from typing import Tuple, Iterable, Type, Any


# 測試組 (名稱, 允許型別)
test_suites: Iterable[Tuple[str, Tuple[Type[Any], ...]]] = [
    ("只允許 float", (float,)),
    ("允許 float, int", (float, int)),
]

# 測資
test_cases = [
    (220.5, 221.0, 219.8),
    (221.0, 208.7, 222.5, 247.6, 223.0, 224.1, 287.3, 225.3),
    (220.1,),
    (221.0, 222.5, 223.0, 224.1, 225.3),
    (),  # 空輸入
    ([219.9, 220.0],),
    ([1.0, 2.0, 3.0],),
    ((1.0, 2.0),),
    ({1.0, 2.0},),
    ({"a": 1.0, "b": 2.0},),
    (1.0, 2.0, 3.0),
    ([1.0, 2.0],),
    ({"a": 1.0},),
    (float("nan"), float("inf"), float("-inf")),
    (1e-308, 1e308),
    ("string", True),
    (123, True),
    ([221.0, "222.5", 223.0], True),
    ((219.9, 220.0, "error"), True),
    ({"voltage": 220.5, "status": "OK"}, True),
    ([None], True),
    ({"a": None}, True),
    ([True, 2.0], True),
    ((object(),), True),
]


def is_valid_case(values: Any, allow_types: Tuple[Type[Any], ...]) -> bool:
    """
    判斷輸入值是否符合 allow_types（遞迴檢查）。
    """
    if isinstance(values, allow_types):
        return True
    if isinstance(values, (list, tuple, set)):
        return all(is_valid_case(v, allow_types) for v in values)
    if isinstance(values, dict):
        return all(is_valid_case(v, allow_types) for v in values.values())
    return False


@pytest.mark.parametrize("suite_name, allow_types", test_suites)
@pytest.mark.parametrize("values", test_cases)
def test_plc_voltage_reader(suite_name, allow_types, values):
    """
    合併正向與負向測試：
    - 符合 allow_types → 不應拋出例外
    - 不符合 allow_types → 應拋出 TypeError
    """
    expect_pass = is_valid_case(values if isinstance(values, tuple) else (values,), allow_types)

    reader = PLCVoltageReader(allow_types=allow_types)
    service = VoltageReaderService(reader)

    if expect_pass:
        # 正向測試
        try:
            voltages = service.collect(values)
            assert isinstance(voltages, tuple)
        except TypeError as e:
            pytest.fail(f"Unexpected TypeError: {e}")
    else:
        # 負向測試
        with pytest.raises(TypeError):
            service.collect(values)


def test_current_jump_strategy_applies_jump(monkeypatch):
    """測試 CurrentJumpStrategy 在時間到時會產生跳動"""

    # 固定 random.uniform 回傳 1.0，避免測試不穩定
    monkeypatch.setattr("random.uniform", lambda a, b: 1.0)

    strategy = CurrentJumpStrategy(lower_bound=-2.0, upper_bound=2.0, interval_sec=0.1)
    reader = PLCVoltageReader(allow_types=(float,), strategy=strategy)
    service = VoltageReaderService(reader)

    inputs = (220.0,)

    # 第一次呼叫 → 會產生跳動 (220.0 + 1.0 = 221.0)
    result1 = service.collect(inputs)
    assert result1 == (221.0,)

    # 馬上呼叫第二次 → 時間未到，應該回傳上一次跳動的值
    result2 = service.collect(inputs)
    assert result2 == result1

    # 等待超過 interval_sec
    import time
    time.sleep(0.11)

    # 再次呼叫 → 會產生跳動
    result3 = service.collect(inputs)
    assert result3 == (221.0,)  # 因為 monkeypatch 固定回傳 1.0


def test_current_jump_strategy_rounding(monkeypatch):
    """測試 round_digits 功能"""

    monkeypatch.setattr("random.uniform", lambda a, b: 0.12345)

    strategy = CurrentJumpStrategy(lower_bound=0, upper_bound=1, interval_sec=0, round_digits=2)
    reader = PLCVoltageReader(allow_types=(float,), strategy=strategy)
    service = VoltageReaderService(reader)

    inputs = (100.0,)

    result = service.collect(inputs)
    # 100.0 + 0.12345 ≈ 100.12 (四捨五入到小數第2位)
    assert result == (100.12,)


def make_service(lower=-1.0, upper=1.0, interval=0.1, round_digits=None):
    """建立帶有 CurrentJumpStrategy 的 service"""
    strategy = CurrentJumpStrategy(lower_bound=lower, upper_bound=upper,
                                   interval_sec=interval, round_digits=round_digits)
    reader = PLCVoltageReader(allow_types=(float,), strategy=strategy)
    return VoltageReaderService(reader)


def test_output_length_matches_input_length_single_value(monkeypatch):
    """輸入單一數值，輸出長度應一致"""
    monkeypatch.setattr("random.uniform", lambda a, b: 0.5)

    service = make_service()
    inputs = (220.0,)
    result = service.collect(inputs)

    assert len(result) == len(inputs), "輸出長度應與輸入一致"


def test_output_length_matches_input_length_multiple_values(monkeypatch):
    """輸入多個數值，輸出長度應一致"""
    monkeypatch.setattr("random.uniform", lambda a, b: 1.0)

    service = make_service()
    inputs = (220.0, 5.0, 110.0)
    result = service.collect(inputs)

    assert len(result) == len(inputs), "輸出長度應與輸入一致"


def test_output_stable_when_interval_not_passed(monkeypatch):
    """在 interval_sec 內呼叫多次 → 輸出長度仍一致"""
    monkeypatch.setattr("random.uniform", lambda a, b: 1.0)

    service = make_service(interval=0.5)
    inputs = (220.0, 5.0)

    result1 = service.collect(inputs)
    result2 = service.collect(inputs)  # 馬上呼叫 → 應該維持上一次的值

    assert len(result1) == len(inputs)
    assert len(result2) == len(inputs)
    assert result1 == result2, "時間未到應該回傳同樣的結果"


def test_output_changes_after_interval(monkeypatch):
    """超過 interval_sec → 應該產生新的跳動值（但長度仍一致）"""
    calls = {"count": 0}

    def fake_uniform(a, b):
        calls["count"] += 1
        return float(calls["count"])  # 每次遞增

    monkeypatch.setattr("random.uniform", fake_uniform)

    service = make_service(interval=0.1)
    inputs = (220.0, 5.0)

    result1 = service.collect(inputs)
    time.sleep(0.11)  # 等超過 interval
    result2 = service.collect(inputs)

    assert len(result1) == len(inputs)
    assert len(result2) == len(inputs)
    assert result1 != result2, "超過 interval 應產生新的值"


def test_strategy_respects_start_delay():
    """測試 start_delay_sec 內不會啟動策略"""
    strategy = CurrentSmoothChangeStrategy(step=1.0, count=3, start_delay_sec=1.0)
    reader = PLCVoltageReader(allow_types=(float,), strategy=strategy)
    service = VoltageReaderService(reader)

    inputs = (100.0,)
    result = service.collect(inputs)

    # 剛開始時應該直接回傳輸入值
    assert result == inputs


def test_strategy_up_direction(monkeypatch):
    """測試 UP 方向：會先遞增再遞減"""
    # 固定 random.uniform = 0，避免隨機性影響
    monkeypatch.setattr("random.uniform", lambda a, b: 0.0)

    strategy = CurrentSmoothChangeStrategy(step=1.0, count=3, start_delay_sec=0.0, direction=Direction.UP)
    reader = PLCVoltageReader(allow_types=(float,), strategy=strategy)
    service = VoltageReaderService(reader)

    inputs = (100.0,)

    # 產生的 wave = [100, 101, 102, 101, 100]
    expected_wave = [100.0, 101.0, 102.0, 101.0, 100.0]

    results = []
    for _ in range(len(expected_wave)):
        results.append(service.collect(inputs)[0])

    assert results == expected_wave


def test_strategy_down_direction(monkeypatch):
    """測試 DOWN 方向：會先遞減再遞增"""
    monkeypatch.setattr("random.uniform", lambda a, b: 0.0)

    strategy = CurrentSmoothChangeStrategy(step=1.0, count=3, start_delay_sec=0.0, direction=Direction.DOWN)
    reader = PLCVoltageReader(allow_types=(float,), strategy=strategy)
    service = VoltageReaderService(reader)

    inputs = (200.0,)

    # 產生的 wave = [200, 199, 198, 199, 200]
    expected_wave = [200.0, 199.0, 198.0, 199.0, 200.0]

    results = []
    for _ in range(len(expected_wave)):
        results.append(service.collect(inputs)[0])

    assert results == expected_wave