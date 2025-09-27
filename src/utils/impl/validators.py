from typing import Any, Iterable, Optional, Type


def _flatten_args(args: Iterable[Any]):
    """展開集合型別為單一序列"""
    for arg in args:
        if isinstance(arg, dict):
            yield from arg.values()
        elif isinstance(arg, (list, tuple, set)) and not isinstance(arg, str):
            yield from arg
        else:
            yield arg


def validate_type(*args: Any, allow_types: Optional[Iterable[Type[Any]]] = None) -> None:
    """
    驗證輸入參數是否符合允許的型別。

    :param allow_types: 可接受的型別清單
    :raises TypeError: 若發現型別不符，則丟出例外
    """
    if allow_types is None:
        return

    for arg in _flatten_args(args):
        if not isinstance(arg, tuple(allow_types)):
            raise TypeError(
                f"Expected one of {[t.__name__ for t in allow_types]}, "
                f"but got {type(arg).__name__}: {arg}"
            )
