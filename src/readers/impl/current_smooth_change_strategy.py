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
        self.step = step
        self.jitter = jitter
        self.count = count
        self.round_digits = round_digits
        self.direction = direction
        self.start_delay_sec = start_delay_sec

        self._start_time = time.time()
        self._active = False
        self._wave_index = 0
        self._base_value = None
        self._wave_values = []

    def _generate_wave(self, base_value: float):
        wave = []

        if self.direction == Direction.UP:
            # 遞增到頂點再遞減
            for i in range(self.count):
                delta = self.step * i + random.uniform(-self.jitter, self.jitter)
                wave.append(round(base_value + delta, self.round_digits))
            for i in range(self.count - 2, -1, -1):
                delta = self.step * i + random.uniform(-self.jitter, self.jitter)
                wave.append(round(base_value + delta, self.round_digits))
        else:
            # 遞減到底再遞增
            for i in range(self.count):
                delta = self.step * i + random.uniform(-self.jitter, self.jitter)
                wave.append(round(base_value - delta, self.round_digits))
            for i in range(self.count - 2, -1, -1):
                delta = self.step * i + random.uniform(-self.jitter, self.jitter)
                wave.append(round(base_value - delta, self.round_digits))

        return wave

    def process(self, currents: Tuple[float, ...]) -> Tuple[float, ...]:
        now = time.time()

        if not self._active:
            if now - self._start_time >= self.start_delay_sec:
                self._active = True
                self._wave_index = 0
                self._base_value = currents[0] if currents else 0.0
                self._wave_values = self._generate_wave(self._base_value)
            else:
                return currents

        if not self._wave_values:
            return currents

        output_value = self._wave_values[self._wave_index]
        self._wave_index += 1

        if self._wave_index >= len(self._wave_values):
            self._wave_index = 0
            self._active = False
            self._start_time = now

        return tuple([output_value])
