from typing import Tuple
from utils.validators import validate_float


class PLCVoltageReader:
    """模擬 PLC 真實讀取資料的實作"""
    def read_values(self, a: float, b: float, c: float) -> Tuple[float, float, float]:
        validate_float(a, b, c)
        # 實務上可在這裡呼叫 PLC API 或硬體讀取
        return (a, b, c)
