from test.mock_reader import MockVoltageReader
from src.services.voltage_service import VoltageService


def main():
    mock_reader = MockVoltageReader()
    voltage_service = VoltageService(mock_reader)

    test_cases = [
        (220.5, 221.0, 219.8),
        (221.0, 208.7, 222.5, 247.6, 223.0, 224.1, 287.3, 225.3),
        (220.1,),
        (221.0, 222.5, 223.0, 224.1, 225.3),
        (),
        (219.9, 220.0),
    ]

    for i, values in enumerate(test_cases, start=1):
        print(f"\n[Test Case {i}] 輸入數值: {values}")
        try:
            result = voltage_service.get_voltage(*values)
            print(f"[Test Case {i}] 模擬輸出: {result}")
        except Exception as e:
            print(f"[Test Case {i}] 發生錯誤: {e}")


if __name__ == "__main__":
    main()
