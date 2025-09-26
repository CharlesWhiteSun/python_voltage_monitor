from typing import Tuple


class PLCVoltageReader:
    """模擬 PLC 真實讀取資料的實作"""

    def read(self, *values: float) -> Tuple[float, ...]:
        print(f"[PLCVoltageReader] 讀取數值: {values}")
        return tuple(values)
