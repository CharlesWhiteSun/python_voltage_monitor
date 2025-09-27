from test.utils.test_validate_type import *


TEST_SUITES = [
    ("utils validate_float 正向測試", test_validate_type_positive),
    ("utils validate_float 負向測試", test_validate_type_negative),
]


def run_all_tests():
    for idx, (title, test_func) in enumerate(TEST_SUITES, start=1):
        print("=" * 60)
        print(f"[{idx}] 執行: {title}")
        print("=" * 60)
        try:
            test_func()
        except Exception as e:
            print(f"[{idx}][X] 測試 {title} 發生錯誤: {e}")
        print("\n")


if __name__ == "__main__":
    run_all_tests()
