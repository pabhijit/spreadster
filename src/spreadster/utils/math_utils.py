from typing import Optional
import math

def round2(x: Optional[float]) -> Optional[float]:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return None
    return round(float(x), 2)

def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
