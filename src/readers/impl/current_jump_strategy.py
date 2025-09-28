import random
import time
from typing import Tuple, Optional


class CurrentJumpStrategy:
    def __init__(
            self, 
            lower_bound: float, 
            upper_bound: float, 
            interval_sec: float = 1.0,
            round_digits: Optional[int] = None,
        ):
        """
        隨機跳動策略
         - 使用 time.time() 檢查距離上次變動的時間是否超過 interval_sec。
         - 如果時間到才變動，否則直接返回原值。

        :param lower_bound: 跳動值的下限
        :param upper_bound: 跳動值的上限
        :param interval_sec: 變動的時間間隔（秒）
        :param round_digits: 四捨五入的小數位數
        """
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.interval_sec = interval_sec
        self.round_digits = round_digits

        self._last_change_time: Optional[float] = None
        self._last_jump_value: Optional[Tuple[float, ...]] = None

    def _apply_round(self, value: float) -> float:
        if self.round_digits is not None:
            return round(value, self.round_digits)
        return value

    def process(self, currents: Tuple[float, ...]) -> Tuple[float, ...]:
        now = time.time()

        # 第一次處理或時間到
        if self._last_change_time is None or (now - self._last_change_time) >= self.interval_sec:
            self._last_change_time = now
            self._last_jump_value = tuple(
                self._apply_round(current + random.uniform(self.lower_bound, self.upper_bound))
                for current in currents
            )
            return self._last_jump_value

        # 時間未到，返回原值
        return currents
