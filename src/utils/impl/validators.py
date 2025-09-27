from typing import Any


def _flatten_args(args):
    """展開集合型別為單一序列"""
    for arg in args:
        if isinstance(arg, dict):
            for v in arg.values():
                yield v
        elif isinstance(arg, (list, tuple, set)):
            for v in arg:
                yield v
        else:
            yield arg


def validate_float(*args: Any, allow: bool = False) -> None:
    """
    驗證輸入參數是否為 float（或 int，視 allow 而定）。

    :raises TypeError: 若發現非 float (或非 int 若 allow=True)，則丟出例外
    """
    for arg in _flatten_args(args):
        if allow and isinstance(arg, int):
            continue
        if not isinstance(arg, float):
            raise TypeError(f"Expected float{' or int' if allow else ''}, but got {type(arg).__name__}: {arg}")

