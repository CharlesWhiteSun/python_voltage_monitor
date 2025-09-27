import pytest
from typing import Tuple, Iterable, Type, Any
from src.readers.impl.plc_voltage_reader import PLCVoltageReader
from src.services.voltage_service import VoltageReaderService


def test_plc_voltage_reader_positive():
    # 定義測試組 (名稱, 允許型別)
    test_suites: Iterable[Tuple[str, Tuple[Type[Any], ...]]] = [
        ("只允許 float", (float,)),
        ("允許 float, int", (float, int)),
    ]

    # 定義所有測資
    test_cases = [
        ((220.5, 221.0, 219.8),),
        ((221.0, 208.7, 222.5, 247.6, 223.0, 224.1, 287.3, 225.3),),
        ((220.1,),),
        ((221.0, 222.5, 223.0, 224.1, 225.3),),
        ((),),  # 空輸入
        (([219.9, 220.0],),),
        (([1.0, 2.0, 3.0],),),
        (((1.0, 2.0),),),
        (({1.0, 2.0},),),
        (({"a": 1.0, "b": 2.0},),),
        ((1.0, 2.0, 3.0),),
        (([1.0, 2.0],),),
        (({"a": 1.0},),),
        ((float("nan"), float("inf"), float("-inf")),),
        ((1e-308, 1e308),),
    ]

    for suite_name, allow_types in test_suites:
        print("=" * 60)
        print(f"執行測試組: {suite_name} (allow_types={allow_types})")
        print("=" * 60)

        reader = PLCVoltageReader(allow_types=allow_types)
        service = VoltageReaderService(reader)

        for idx, (values,) in enumerate(test_cases, start=1):
            # 自動判斷是否通過型別驗證
            def is_valid(value: Any) -> bool:
                if isinstance(value, allow_types):
                    return True
                if isinstance(value, (list, tuple, set)):
                    return all(is_valid(v) for v in value)
                if isinstance(value, dict):
                    return all(is_valid(v) for v in value.values())
                return False

            expect_pass = is_valid(values if isinstance(values, tuple) else (values,))

            print(f"[{suite_name}][Test Case {idx}] 輸入數值: {values}, expect_pass={expect_pass}")
            try:
                voltages = service.collect(*values)
                print(f"[{suite_name}][Test Case {idx}] ✅ 電壓讀取結果: {voltages}")
                if not expect_pass:
                    pytest.fail(f"[{suite_name}][Test Case {idx}] 本應失敗，卻通過了")
            except Exception as e:
                print(f"[{suite_name}][Test Case {idx}] ❌ 發生錯誤: {e}")
                if expect_pass:
                    pytest.fail(f"[{suite_name}][Test Case {idx}] 本應通過，卻失敗了: {e}")


def test_plc_voltage_reader_negative():
    test_suites = [
        ("只允許 float", (float,)),
        ("允許 float, int", (float, int)),
    ]

    test_cases = [
        ("string", False),
        (123, False),
        ([221.0, "222.5", 223.0], False),
        ((219.9, 220.0, "error"), False),
        ({"voltage": 220.5, "status": "OK"}, False),
        ([None], False),
        ({"a": None}, False),
        ([True, 2.0], False),
        ((object(),), False),
    ]

    print("=" * 60)
    print("[PLCVoltageReader] 負向測試")

    for suite_name, allow_types in test_suites:
        print("=" * 60)
        print(f"執行測試組: {suite_name} (allow_types={allow_types})")

        reader = PLCVoltageReader(allow_types=allow_types)
        service = VoltageReaderService(reader)

        for idx, (values, expect_fail) in enumerate(test_cases, start=1):
            print(f"[{suite_name}][Test Case {idx}] 輸入數值: {values}, expect_fail={expect_fail}")
            try:
                voltages = service.collect(*values, allow=False)
            except Exception as e:
                print(f"[{suite_name}][Test Case {idx}] ✅ 正確觸發錯誤: {e}")
            else:
                if expect_fail:
                    print(f"[{suite_name}][Test Case {idx}] ❌ 沒有觸發錯誤，結果: {voltages}")
                    pytest.fail("Negative test failed: 沒有觸發錯誤")
                else:
                    print(f"[{suite_name}][Test Case {idx}] ✅ 測試通過")
