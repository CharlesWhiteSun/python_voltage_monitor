from src.readers.interfaces import IValidatingReader
from src.utils.impl.validators import validate_type
from typing import Any, Iterable, Optional, Tuple, Type


class PLCVoltageReader(IValidatingReader):
    """模擬 PLC 真實讀取資料，並檢查輸入型別"""
    allow_types: Optional[Iterable[Type[Any]]]

    def __init__(self, allow_types: Optional[Iterable[Type[Any]]] = None) -> None:
        self.allow_types = allow_types

    def validate(self, *values: Any) -> None:
        if self.allow_types is None:
            return
        validate_type(*values, allow_types=self.allow_types)

    def read(self, *values: Any) -> Tuple[Any, ...]:
        print(f"[{self.__class__.__name__}] 讀取數值: {values}")
        return tuple(values)
