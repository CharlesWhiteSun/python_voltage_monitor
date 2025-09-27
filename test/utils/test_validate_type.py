import pytest
from src.utils.impl.validators import validate_type


def test_validate_type_positive():
    """正向測試 — 所有輸入型別符合允許型別時不會拋錯"""
    test_cases_float_only = [
        (1.0, 2.5, 3.14159),
        ([1.0, 2.0, 3.0],),
        ((1.0, 2.0),),
        ({1.0, 2.0},),
        ({"a": 1.0, "b": 2.0},),
        (),  # 空集合
    ]

    test_cases_float_int = [
        (1, 2, 3),
        ([1, 2.0],),
        ({"a": 1},),
    ]

    allow_types_cases = [
        ("只允許 float", (float,), test_cases_float_only),
        ("允許 float, int", (float, int), test_cases_float_only + test_cases_float_int),
    ]

    print("=" * 60)
    print("[validate_type] 正向測試")

    for suite_name, allow_types, cases in allow_types_cases:
        print("=" * 60)
        print(f"執行測試組: {suite_name} (allow_types={allow_types})")

        for idx, values in enumerate(cases, start=1):
            print(f"[{suite_name}][Test Case {idx}] 輸入: {values}")
            try:
                validate_type(*values, allow_types=allow_types)
                print(f"[{suite_name}][Test Case {idx}] ✅ 測試通過")
            except TypeError as e:
                pytest.fail(f"[{suite_name}][Test Case {idx}] ❌ 發生錯誤: {e}")


def test_validate_type_negative():
    """負向測試 — 輸入型別不符合允許型別時必須拋出 TypeError"""

    test_cases = [
        ("string",),                     # str
        ([1.0, "2.0", 3.0],),
        ((219.9, 220.0, "error"),),
        ({"voltage": 220.5, "status": "OK"},),
        ([None],),
        ({"a": None},),
        ([[], 2.0],),  # list 含 list，必定錯誤
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
            print(f"[{suite_name}][Test Case {idx}] 輸入: {values}")
            with pytest.raises(TypeError) as exc_info:
                validate_type(*values, allow_types=allow_types)
            print(f"[{suite_name}][Test Case {idx}] ✅ 正確拋出 TypeError: {exc_info.value}")
