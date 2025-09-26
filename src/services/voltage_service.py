from typing import Tuple
from src.readers.interfaces import IReader


class VoltageReaderService:
    """
    接受任何符合 IReader 的實作。
    """

    def __init__(self, reader: IReader):
        self.reader = reader

    def collect(self, *values: float) -> Tuple[float, ...]:
        return self.reader.read(*values)
