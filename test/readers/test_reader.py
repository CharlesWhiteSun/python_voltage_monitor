import pytest
from src.readers.impl.plc_voltage_reader import PLCVoltageReader
from src.services.voltage_service import VoltageReaderService


def test_plc_voltage_reader_positive():
    reader = PLCVoltageReader()
    service = VoltageReaderService(reader)

    test_cases = [
        ( (220.5, 221.0, 219.8), False ),
        ( (221.0, 208.7, 222.5, 247.6, 223.0, 224.1, 287.3, 225.3), False ),
        ( (220.1,), False ),
        ( (221.0, 222.5, 223.0, 224.1, 225.3), False ),
        ( (), False ),  # 空輸入
        ( ([219.9, 220.0],), False ),
        ( ([1.0, 2.0, 3.0],), False ),
        ( ((1.0, 2.0),), False ),
        ( ({1.0, 2.0},), False ),
        ( ({"a": 1.0, "b": 2.0},), False ),
        ( (1, 2, 3), True ),   # allow=True
        ( ([1, 2.0],), True ),
        ( ({"a": 1},), True ),
        ( (float("nan"), float("inf"), float("-inf")), False ),  # 邊際值
        ( (1e-308, 1e308), False ),  # 極限值
    ]

    for idx, (values, allow) in enumerate(test_cases, start=1):
        print(f"[Test Case {idx}] 輸入數值: {values}, allow={allow}")
        try:
            voltages = service.collect(*values, allow=allow)
            print(f"[Test Case {idx}] ✅ 電壓讀取結果: {voltages}")
        except Exception as e:
            print(f"[Test Case {idx}] ❌ 發生錯誤: {e}")
            pytest.fail(f"Positive test failed: {e}")


def test_plc_voltage_reader_negative():
    reader = PLCVoltageReader()
    service = VoltageReaderService(reader)

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

    for idx, (values, allow) in enumerate(test_cases, start=1):
        print(f"[Test Case {idx}] 輸入數值: {values}, allow={allow}")
        try:
            voltages = service.collect(*values, allow=allow)
        except Exception as e:
            print(f"[Test Case {idx}] ✅ 正確觸發錯誤: {e}")
        else:
            print(f"[Test Case {idx}] ❌ 沒有觸發錯誤，讀取結果: {voltages}")
            pytest.fail(f"Negative test failed: 沒有觸發錯誤")
