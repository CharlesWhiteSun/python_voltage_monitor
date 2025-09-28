from typing import Optional, Protocol, Iterable, Type, Tuple, Any


class IValidator(Protocol):
    """介面: 定義檢查輸入參數型別的方法"""
    def validate(self, *values: Any) -> None:
        """如果型別錯誤，應丟出對應的 Exception。"""


class ITypeCheckValidator(IValidator, Protocol):
    """介面: 型別檢查的設定"""
    allow_types: Optional[Iterable[Type[Any]]]


class IReader(Protocol):
    """介面: 定義讀取多組任意型別的方法"""
    def read(self, *values: Any) -> Tuple[Any, ...]:
        ...


class IValidatingReader(IReader, ITypeCheckValidator, Protocol):
    """合併介面"""


class ICurrentProcessingStrategy(Protocol):
    """介面: 定義電流處理策略"""
    def process(self, currents: Tuple[float, ...]) -> Tuple[float, ...]:
        ...