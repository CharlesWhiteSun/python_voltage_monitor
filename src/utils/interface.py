from typing import Protocol, Any

class IValidator(Protocol):
    def validate(self, *values: Any) -> None:
        """驗證器，如果錯誤應丟出對應的 Exception"""
