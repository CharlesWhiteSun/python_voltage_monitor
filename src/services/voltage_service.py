from typing import Optional, Tuple, Iterable, Type, Any
from src.readers.interfaces import IValidatingReader


class VoltageReaderService:
    """接受任何符合 IValidatingReader 的實作。"""
    def __init__(self, reader: IValidatingReader):
        self.reader = reader

    def collect(self, values: Any, allow_types: Optional[Iterable[Type[Any]]] = None) -> Tuple[Any, ...]:
        if isinstance(values, dict):
            values = tuple(values.values())
        elif isinstance(values, (list, tuple, set)):
            values = tuple(values)
        else:
            values = (values,)

        allow_types = allow_types or getattr(self.reader, "allow_types", None)
        if hasattr(self.reader, "allow_types"):
            self.reader.allow_types = allow_types

        self.reader.validate(*values)
        return self.reader.read(*values)
