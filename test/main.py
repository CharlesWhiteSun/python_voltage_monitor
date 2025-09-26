from test.test_reader import test_plc_voltage_reader


TEST_SUITES = [
    ("PLC Voltage Reader 測試", test_plc_voltage_reader),
]


def run_all_tests():
    for idx, (title, test_func) in enumerate(TEST_SUITES, start=1):
        print("=" * 60)
        print(f"[{idx}] 執行: {title}")
        print("=" * 60)
        try:
            test_func()
        except Exception as e:
            print(f"[{idx}] 測試 {title} 發生錯誤: {e}")
        print("\n")


if __name__ == "__main__":
    run_all_tests()
