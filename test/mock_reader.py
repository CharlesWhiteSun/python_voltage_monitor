from typing import Tuple
from src.utils.validators import validate_float


class MockVoltageReader:
    """測試用的假資料實作"""
    def read_values(self, a: float, b: float, c: float) -> Tuple[float, float, float]:
        validate_float(a, b, c)
        return (a + 0.1, b + 0.1, c + 0.1)


if __name__ == "__main__":
    reader = MockVoltageReader()
    test_values = (220.5, 221.0, 219.8)
    print(f"Testing MockVoltageReader with values: {test_values}")
    results = reader.read_values(*test_values)
    print(f"Output: {results}")