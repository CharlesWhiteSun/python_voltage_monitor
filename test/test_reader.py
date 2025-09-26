from src.readers.impl.plc_voltage_reader import PLCVoltageReader
from src.services.voltage_service import VoltageReaderService


def test_plc_voltage_reader():
    reader = PLCVoltageReader()
    service = VoltageReaderService(reader)

    test_cases = [
        (220.5, 221.0, 219.8),
        (221.0, 208.7, 222.5, 247.6, 223.0, 224.1, 287.3, 225.3),
        (220.1,),
        (221.0, 222.5, 223.0, 224.1, 225.3),
        (),
        (219.9, 220.0),
    ]

    for idx, values in enumerate(test_cases, start=1):
        print(f"[Test Case {idx}] 輸入數值: {values}")
        try:
            voltages = service.collect(*values)
            print(f"[Test Case {idx}] 電壓讀取結果: {voltages}")
        except Exception as e:
            print(f"[Test Case {idx}] 發生錯誤: {e}")
