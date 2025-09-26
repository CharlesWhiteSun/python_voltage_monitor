from typing import Protocol, Tuple


class VoltageReader(Protocol):
    """
    介面: 定義讀取多組 float 的方法
    """
    def read(self, *values: float) -> Tuple[float, ...]:
        ...