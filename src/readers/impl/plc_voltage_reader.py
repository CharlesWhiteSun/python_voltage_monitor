from src.readers.interfaces import IValidatingReader
from src.utils.impl.validators import validate_float
from typing import Any, Tuple


class PLCVoltageReader(IValidatingReader):
    """模擬 PLC 真實讀取資料，並檢查輸入型別"""

    def __init__(self, allow: bool = False):
        self.allow = allow

    def validate(self, *values: Any) -> None:
        validate_float(*values, allow=self.allow)

    def read(self, *values: float) -> Tuple[float, ...]:
        print(f"[{self.__class__.__name__}] 讀取數值: {values}")
        return tuple(values)
