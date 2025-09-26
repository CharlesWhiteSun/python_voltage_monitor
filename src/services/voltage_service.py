from typing import Tuple
from readers.interfaces import VoltageReader


class VoltageService:
    """高階邏輯，透過依賴注入接收不同的 Reader"""
    def __init__(self, reader: VoltageReader) -> None:
        self.reader = reader

    def get_voltage(self, a: float, b: float, c: float) -> Tuple[float, float, float]:
        return self.reader.read_values(a, b, c)
