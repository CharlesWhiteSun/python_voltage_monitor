from typing import Protocol, Tuple, Any


class IValidator(Protocol):
    """介面: 定義檢查輸入參數型別的方法"""
    def validate(self, *values: Any) -> None:
        """如果型別錯誤，應丟出對應的 Exception。"""


class ITypeCheckValidator(IValidator, Protocol):
    """介面: 繼承 IValidator，並加入型別檢查的設定"""
    allow: bool


class IReader(Protocol):
    """介面: 定義讀取多組 float 的方法"""
    def read(self, *values: float) -> Tuple[float, ...]:
        ...


class IValidatingReader(IReader, ITypeCheckValidator, Protocol):
    """合併介面"""
