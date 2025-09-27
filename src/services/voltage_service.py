from typing import Tuple
from src.readers.interfaces import IValidatingReader


class VoltageReaderService:
    """接受任何符合 IValidatingReader 的實作。"""
    def __init__(self, reader: IValidatingReader):
        self.reader = reader
    
    def collect(self, *values: float, allow: bool = False) -> Tuple[float, ...]:
        if hasattr(self.reader, "allow"):
            self.reader.allow = allow
        self.reader.validate(*values)
        return self.reader.read(*values)
