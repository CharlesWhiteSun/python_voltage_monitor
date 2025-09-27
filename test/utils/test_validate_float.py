import pytest
from src.utils.impl.validators import validate_float


def test_validate_float_positive():
    test_cases = [
        (1.0, 2.5, 3.14159),
        (),
        (1e-308, 1e308),
        (float("nan"), float("inf"), float("-inf")),
        ([1.0, 2.0, 3.0],),
        ((1.0, 2.0),),
        ({1.0, 2.0},),
        ({"a": 1.0, "b": 2.0},),
        (1, 2, 3),      # allow_int=True
        ([1, 2.0],),    # allow_int=True
        ({"a": 1},),    # allow_int=True
    ]

    allow_int_cases = {9, 10, 11}  # 指定哪個 case 允許 int

    for idx, values in enumerate(test_cases, start=1):
        allow_int = idx in allow_int_cases
        print(f"[Test Case {idx}] 輸入數值: {values} allow_int={allow_int}")
        try:
            validate_float(*values, allow=allow_int)
            print(f"[Test Case {idx}] ✅ 測試通過")
        except Exception as e:
            print(f"[Test Case {idx}] ❌ 發生錯誤: {e}")
            pytest.fail(f"Positive test failed: {e}")


def test_validate_float_negative():
    test_cases = [
        (2,),               # int
        (1.0, 2),           # int
        ("bad",),           # string
        (None,),            # None
        ([1.0, "oops"],),   # list mixed
        ((1.0, 2),),        # tuple mixed
        ({1.0, "bad"},),    # set mixed
        ({"a": "bad"},),    # dict invalid
        ("bad",),           # string with allow_int=True
    ]

    allow_int_cases = {8}  # 指定哪些 case 開啟 allow_int=True

    for idx, values in enumerate(test_cases, start=1):
        allow_int = idx in allow_int_cases
        print(f"[Test Case {idx}] 輸入數值: {values} allow_int={allow_int}")
        try:
            validate_float(*values, allow=allow_int)
            print(f"[Test Case {idx}] ❌ 測試失敗，預期 TypeError")
            pytest.fail("Expected TypeError but no exception was raised")
        except TypeError as e:
            print(f"[Test Case {idx}] ✅ 正確拋出 TypeError: {e}")
        except Exception as e:
            print(f"[Test Case {idx}] ❌ 發生其他錯誤: {e}")
            pytest.fail(f"Unexpected error type: {e}")
