import pytest
from src.utils.impl.validators import _flatten_args, validate_type

def test_validate_type_positive():
    test_cases = [
        (1.0, 2.5, 3.14159),
        (),
        (1e-308, 1e308),
        (float("nan"), float("inf"), float("-inf")),
        ([1.0, 2.0, 3.0],),
        ((1.0, 2.0),),
        ({1.0, 2.0},),
        ({"a": 1.0, "b": 2.0},),
        (1, 2, 3),      # allow int
        ([1, 2.0],),    # allow int
        ({"a": 1},),    # allow int
    ]

    allow_types_cases = [
        ("只允許 float", (float,)),
        ("允許 float, int", (float, int)),
    ]

    allow_int_cases = {9, 10, 11}  # 指定哪些 case 允許 int

    print("=" * 60)
    print("[validate_type] 正向測試")

    for suite_name, allow_types in allow_types_cases:
        print("=" * 60)
        print(f"執行測試組: {suite_name} (allow_types={allow_types})")

        for idx, values in enumerate(test_cases, start=1):
            should_pass = True
            if allow_types == (float,) and idx in allow_int_cases:
                should_pass = False  # 浮點限制下，允許 int 的 case 應該 fail

            print(f"[{suite_name}][Test Case {idx}] 輸入: {values}")
            try:
                validate_type(*values, allow_types=allow_types)
                if not should_pass:
                    print(f"[{suite_name}][Test Case {idx}] ❌ 預期失敗但通過")
                    pytest.fail("Expected TypeError but no exception was raised")
                else:
                    print(f"[{suite_name}][Test Case {idx}] ✅ 測試通過")
            except TypeError as e:
                if should_pass:
                    print(f"[{suite_name}][Test Case {idx}] ❌ 發生錯誤: {e}")
                    pytest.fail(f"Positive test failed: {e}")
                else:
                    print(f"[{suite_name}][Test Case {idx}] ✅ 正確拋出 TypeError: {e}")


def test_validate_type_negative():
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

    allow_types_cases = [
        ("只允許 float", (float,)),
        ("允許 float, int", (float, int)),
    ]

    print("=" * 60)
    print("[validate_type] 負向測試")

    for suite_name, allow_types in allow_types_cases:
        print("=" * 60)
        print(f"執行測試組: {suite_name} (allow_types={allow_types})")

        for idx, values in enumerate(test_cases, start=1):
            should_fail = False
            for arg in values:
                for val in _flatten_args([arg]):
                    if not isinstance(val, tuple(allow_types)):
                        should_fail = True
                        break
                if should_fail:
                    break

            print(f"[{suite_name}][Test Case {idx}] 輸入: {values} should_fail={should_fail}")

            try:
                validate_type(*values, allow_types=allow_types)
                if should_fail:
                    print(f"[{suite_name}][Test Case {idx}] ❌ 測試失敗，預期 TypeError")
                    pytest.fail("Expected TypeError but no exception was raised")
                else:
                    print(f"[{suite_name}][Test Case {idx}] ✅ 測試通過")
            except TypeError as e:
                if should_fail:
                    print(f"[{suite_name}][Test Case {idx}] ✅ 正確拋出 TypeError: {e}")
                else:
                    print(f"[{suite_name}][Test Case {idx}] ❌ 不應該拋出 TypeError: {e}")
                    pytest.fail(f"Unexpected TypeError: {e}")
            except Exception as e:
                print(f"[{suite_name}][Test Case {idx}] ❌ 發生其他錯誤: {e}")
                pytest.fail(f"Unexpected error type: {e}")
