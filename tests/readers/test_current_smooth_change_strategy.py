import time
import pytest
from typing import Tuple
from python_voltage_monitor.readers.impl.current_smooth_change_strategy import (
    CurrentSmoothChangeStrategy,
    Direction
)


@pytest.mark.parametrize("direction", [Direction.UP, Direction.DOWN])
def test_wave_generation(direction):
    strategy = CurrentSmoothChangeStrategy(
        step=2.0,
        jitter=0.0,
        count=5,
        round_digits=1,
        direction=direction,
        start_delay_sec=0.0
    )

    base_values: Tuple[float, ...] = (10.0, 10.0)  # <-- 傳入 tuple，而不是單一 float
    outputs = []

    # 產生一個完整的波形週期
    for _ in range((strategy.count * 2) - 1):
        out = strategy.process(base_values)
        outputs.append(out[0])

    # 波形長度應該等於 count*2 - 1
    assert len(outputs) == (strategy.count * 2) - 1

    if direction == Direction.UP:
        assert outputs[0] < outputs[strategy.count - 1]  # 遞增
        assert outputs[strategy.count - 1] > outputs[-1]  # 遞減
    else:
        assert outputs[0] > outputs[strategy.count - 1]  # 遞減
        assert outputs[strategy.count - 1] < outputs[-1]  # 遞增


@pytest.mark.slow
def test_start_delay_behavior():
    strategy = CurrentSmoothChangeStrategy(
        step=1.0,
        jitter=0.0,
        count=5,
        round_digits=1,
        direction=Direction.UP,
        start_delay_sec=1.0
    )

    inputs = (10.0,)
    first_output = strategy.process(inputs)

    # 還沒到啟動時間，輸出應該等於輸入
    assert first_output == inputs
    assert strategy._active is False

    time.sleep(1.1)  # 等待啟動
    second_output = strategy.process(inputs)

    # 啟動後，active 應該為 True
    assert strategy._active is True

    # 第二次輸出應該進入波形變化
    third_output = strategy.process(inputs)
    assert third_output != inputs


def test_round_digits_and_jitter():
    strategy = CurrentSmoothChangeStrategy(
        step=1.0,
        jitter=0.5,
        count=5,
        round_digits=1,
        direction=Direction.UP,
        start_delay_sec=0.0
    )

    inputs = (10.0,)  # 明確給 tuple
    values = []

    # 產生一個完整波形
    for _ in range((strategy.count * 2) - 1):
        out = strategy.process(inputs)
        # 確認回傳 tuple 長度與輸入相同
        assert len(out) == len(inputs)
        values.append(out[0])

    # 檢查數值小數位數
    for val in values:
        decimal_part = str(val).split(".")[1] if "." in str(val) else ""
        assert len(decimal_part) <= 1

    # 檢查 jitter 是否影響波形（數值會有微小變化）
    diffs = [abs(values[i + 1] - values[i]) for i in range(len(values) - 1)]
    assert any(diff != 1.0 for diff in diffs)  # jitter 導致的差異


def test_wave_cycle_repeat():
    strategy = CurrentSmoothChangeStrategy(
        step=1.0,
        jitter=0.0,
        count=3,
        round_digits=1,
        direction=Direction.UP,
        start_delay_sec=0.0
    )

    inputs = (10.0,)

    first_cycle = [strategy.process(inputs)[0] for _ in range((strategy.count * 2) - 1)]
    second_cycle = [strategy.process(inputs)[0] for _ in range((strategy.count * 2) - 1)]

    # jitter=0，生成的波形應該完全相同
    assert first_cycle == second_cycle
    # 波形長度要正確
    assert len(first_cycle) == (strategy.count * 2) - 1
