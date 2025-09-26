def validate_float(*args) -> None:
    """驗證輸入參數必須為 float"""
    for arg in args:
        if not isinstance(arg, float):
            raise TypeError(f"Expected float, but got {type(arg).__name__}: {arg}")
