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

    base_value = 10.0
    inputs: Tuple[float, ...] = (base_value,)
    outputs = []

    # 產生一個完整的波形週期
    for _ in range((strategy.count * 2) - 1):
        out = strategy.process(inputs)
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

    inputs = (10.0,)
    values = [strategy.process(inputs)[0] for _ in range((strategy.count * 2) - 1)]

    # 檢查數值小數位數
    for val in values:
        decimal_part = str(val).split(".")[1] if "." in str(val) else ""
        assert len(decimal_part) <= 1

    # 檢查 jitter 是否影響波形（數值會有微小變化）
    diffs = [abs(values[i+1] - values[i]) for i in range(len(values)-1)]
    assert any(diff != 2.0 for diff in diffs)  # jitter導致的差異


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

    assert first_cycle == second_cycle  # jitter=0 無隨機波動，週期應相同
