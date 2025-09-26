from typing import Tuple
from src.readers.interfaces import VoltageReader


class MockVoltageReader(VoltageReader):
    """測試用的假資料實作"""

    def read(self, *values: float) -> Tuple[float, ...]:
        print(f"[MockVoltageReader] 模擬讀取數值: {values}")
        return tuple(v + 0.99999 for v in values)
