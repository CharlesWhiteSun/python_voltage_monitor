from typing import Protocol, Tuple


class VoltageReader(Protocol):
    """介面: 定義讀取三組 float 的方法"""
    def read_values(self, a: float, b: float, c: float) -> Tuple[float, float, float]:
        ...
