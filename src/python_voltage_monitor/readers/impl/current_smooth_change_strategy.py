import time
import random
from typing import Tuple
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = -1


class CurrentSmoothChangeStrategy:
    def __init__(
        self,
        step: float = 1.0,
        jitter: float = 0.0,
        count: int = 20,
        round_digits: int = 2,
        direction: Direction = Direction.UP,
        start_delay_sec: float = 1.0,
    ):
        """
        平滑變動策略
        - 輸入多少個參數，就對每個參數套用一樣的波動邏輯
        - 每個輸出值會依據 base_value + 波動量計算
        - 確保輸入與輸出參數數量一致
        
        :param step: 每次變動的步長
        :param jitter: 每次變動的隨機抖動範圍
        :param count: 每個波動週期的步數
        :param round_digits: 四捨五入的小數位數
        :param direction: 變動方向（UP 或 DOWN）
        :param start_delay_sec: 啟動後延遲多長時間開始變動（秒）
        """
        self.step = step
        self.jitter = jitter
        self.count = count
        self.round_digits = round_digits
        self.direction = direction
        self.start_delay_sec = start_delay_sec

        self._start_time = time.time()
        self._active = False
        self._wave_index = 0
        self._base_values: Tuple[float, ...] = ()
        self._wave_values: Tuple[Tuple[float, ...], ...] = ()

    def _generate_wave(self, base_values: Tuple[float, ...]) -> Tuple[Tuple[float, ...], ...]:
        """
        為每個 base_value 生成一組平滑波動，最後組合成多維輸出
        """
        waves = []

        for base in base_values:
            wave = []
            if self.direction == Direction.UP:
                # 遞增到頂點再遞減
                for i in range(self.count):
                    delta = self.step * i + random.uniform(-self.jitter, self.jitter)
                    wave.append(round(base + delta, self.round_digits))
                for i in range(self.count - 2, -1, -1):
                    delta = self.step * i + random.uniform(-self.jitter, self.jitter)
                    wave.append(round(base + delta, self.round_digits))
            else:
                # 遞減到底再遞增
                for i in range(self.count):
                    delta = self.step * i + random.uniform(-self.jitter, self.jitter)
                    wave.append(round(base - delta, self.round_digits))
                for i in range(self.count - 2, -1, -1):
                    delta = self.step * i + random.uniform(-self.jitter, self.jitter)
                    wave.append(round(base - delta, self.round_digits))
            waves.append(wave)

        # zip 每個 step 的多個 wave，形成多維輸出
        return tuple(zip(*waves))

    def process(self, currents: Tuple[float, ...]) -> Tuple[float, ...]:
        now = time.time()

        if not self._active:
            if now - self._start_time >= self.start_delay_sec:
                self._active = True
                self._wave_index = 0
                self._base_value = currents
                self._wave_values = self._generate_wave(self._base_value)
            else:
                return currents

        if not self._wave_values:
            return currents

        output_values = self._wave_values[self._wave_index]
        self._wave_index += 1

        if self._wave_index >= len(self._wave_values):
            self._wave_index = 0
            self._active = False
            self._start_time = now

        return tuple(output_values)
