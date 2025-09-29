from python_voltage_monitor.readers.interfaces import IValidatingReader, ICurrentProcessingStrategy
from python_voltage_monitor.utils.validators import validate_type
from typing import Any, Iterable, Optional, Tuple, Type


class PLCVoltageReader(IValidatingReader):
    """模擬 PLC 真實讀取資料，並檢查輸入型別"""
    allow_types: Optional[Iterable[Type[Any]]]

    def __init__(
            self, 
            allow_types: Optional[Iterable[Type[Any]]] = None,
            strategy: Optional[ICurrentProcessingStrategy] = None
        ) -> None:
        self.allow_types = allow_types
        self.strategy = strategy

    def set_strategy(self, strategy: ICurrentProcessingStrategy) -> None:
        self.strategy = strategy

    def validate(self, *values: Any) -> None:
        if self.allow_types is None:
            return
        validate_type(*values, allow_types=self.allow_types)

    def read(self, *values: Any) -> Tuple[Any, ...]:
        self.validate(*values)
        print(f"[{self.__class__.__name__}] 原始數值: {values}")

        if self.strategy:
            processed_values = self.strategy.process(tuple(values))
            print(f"[{self.__class__.__name__}] 處理後數值: {processed_values}")
            return processed_values

        return tuple(values)
