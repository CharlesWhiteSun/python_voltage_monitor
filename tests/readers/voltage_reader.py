import pytest
from typing import Tuple, Iterable, Type, Any
from src.readers.impl.plc_voltage_reader import PLCVoltageReader
from src.services.voltage_service import VoltageReaderService


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
