from typing import Tuple
from src.readers.interfaces import VoltageReader


class VoltageService:
    """
    VoltageService 接受任何符合 VoltageReader 的實作。
    """

    def __init__(self, reader: VoltageReader):
        self.reader = reader

    def get_voltage(self, *values: float) -> Tuple[float, ...]:
        return self.reader.read(*values)
