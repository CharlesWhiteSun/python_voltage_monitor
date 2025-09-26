from typing import Protocol, Tuple


class IReader(Protocol):
    """
    介面: 定義讀取多組 float 的方法
    """
    def read(self, *values: float) -> Tuple[float, ...]:
        ...