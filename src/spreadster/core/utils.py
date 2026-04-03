from __future__ import annotations
from datetime import datetime
import math
from typing import Optional

MONTH_ABBR = {
    1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
    7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"
}

def tos_date_str(expiration: str) -> str:
    ts = datetime.fromisoformat(expiration)
    return f"{ts.day:02d} {MONTH_ABBR[ts.month]} {str(ts.year)[-2:]}"

def pct_profit(entry_credit: float, current_value: float) -> float:
    if entry_credit <= 0:
        return 0.0
    return round((entry_credit - current_value) / entry_credit, 4)

def round2(x: Optional[float]) -> Optional[float]:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return None
    return round(float(x), 2)
