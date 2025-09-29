import time
import pytest
from typing import Tuple
from python_voltage_monitor.readers.impl.current_jump_strategy import CurrentJumpStrategy


@pytest.mark.slow
def test_jump_strategy_changes_after_interval():
    """測試時間到時跳動發生"""
    strategy = CurrentJumpStrategy(lower_bound=-0.5, upper_bound=0.5, interval_sec=0.5, round_digits=2)

    inputs: Tuple[float, ...] = (220.0, 221.0, 219.8)

    # 第一次呼叫，必定變動
    output1 = strategy.process(inputs)
    assert output1 != inputs, "第一次應該變動"

    # 驗證四捨五入
    for out in output1:
        assert isinstance(out, float)
        assert len(str(out).split(".")[1]) <= 2, "輸出應四捨五入到 2 位小數"

    # 立即呼叫，時間未到，應返回原值
    output2 = strategy.process(inputs)
    assert output2 == inputs, "時間未到，應該返回原值"

    # 等到時間到，再呼叫，應該變動
    time.sleep(0.6)
    output3 = strategy.process(inputs)
    assert output3 != inputs, "時間到，應該變動"
    assert output3 != output1, "應該產生新的跳動值"


def test_jump_strategy_empty_input():
    """測試空輸入處理"""
    strategy = CurrentJumpStrategy(lower_bound=-0.5, upper_bound=0.5, interval_sec=1.0, round_digits=3)
    inputs: Tuple[float, ...] = ()

    output = strategy.process(inputs)
    assert output == (), "空輸入應返回空 tuple"


def test_jump_strategy_bounds():
    """測試跳動值是否在上下限範圍內"""
    lower = -1.0
    upper = 1.0
    strategy = CurrentJumpStrategy(lower_bound=lower, upper_bound=upper, interval_sec=0.1, round_digits=2)

    inputs: Tuple[float, ...] = (220.0, 221.0, 219.8)
    output = strategy.process(inputs)

    for inp, out in zip(inputs, output):
        diff = round(out - inp, 2)
        assert lower <= diff <= upper, f"跳動差值 {diff} 不在 {lower}~{upper} 範圍"


@pytest.mark.slow
def test_jump_strategy_interval_logic():
    """測試時間間隔邏輯"""
    strategy = CurrentJumpStrategy(lower_bound=-0.5, upper_bound=0.5, interval_sec=0.2, round_digits=1)

    inputs: Tuple[float, ...] = (220.0,)
    output1 = strategy.process(inputs)
    time.sleep(0.1)
    output2 = strategy.process(inputs)
    time.sleep(0.2)
    output3 = strategy.process(inputs)

    assert output1 != inputs, "第一次應變動"
    assert output2 == inputs, "時間未到應保持原值"
    assert output3 != inputs, "時間到應變動"


@pytest.mark.parametrize("lower, upper, digits", [(-0.5, 0.5, 1), (-1.0, 1.0, 2), (-0.2, 0.2, 3)])
def test_jump_strategy_param_bounds(lower, upper, digits):
    """測試不同上下限與小數位數參數"""
    strategy = CurrentJumpStrategy(lower_bound=lower, upper_bound=upper, interval_sec=0.1, round_digits=digits)

    inputs: Tuple[float, ...] = (220.0, 221.0, 219.8)
    output = strategy.process(inputs)

    for inp, out in zip(inputs, output):
        diff = out - inp
        assert lower <= diff <= upper, f"跳動差值 {diff} 不在 {lower}~{upper} 範圍"


@pytest.mark.slow
def test_jump_strategy_print_results():
    strategy = CurrentJumpStrategy(lower_bound=200, upper_bound=400, interval_sec=2.0, round_digits=1)

    inputs: Tuple[float, ...] = (
        220.0, 221.0, 219.8, 220.1, 221.5, 223.0, 224.1, 225.3, 226.7, 228.0,
        220.0, 221.0, 219.8, 220.1, 221.5, 223.0, 224.1, 225.3, 226.7, 228.0,
        220.0, 221.0, 219.8, 220.1, 221.5, 223.0, 224.1, 225.3, 226.7, 228.0,
        220.0, 221.0, 219.8, 220.1, 221.5, 223.0, 224.1, 225.3, 226.7, 228.0,
        220.0, 221.0, 219.8, 220.1, 221.5, 223.0, 224.1, 225.3, 226.7, 228.0,
    )

    for i, value in enumerate(inputs):
        output = strategy.process((value,))
        print(f"[{i}] 輸入: {value} -> 輸出: {output[0]}")
        time.sleep(0.25)
