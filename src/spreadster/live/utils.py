from __future__ import annotations
from spreadster.utils.dates import tos_date_str

def pct_profit(entry_credit: float, current_value: float) -> float:
    if entry_credit <= 0:
        return 0.0
    return round((entry_credit - current_value) / entry_credit, 4)

def side_close_code(symbol: str, expiration: str, option_type: str, short_strike: float, long_strike: float, quantity: int, limit_price: float, weeklys: bool = True) -> str:
    wk = " (Weeklys)" if weeklys else ""
    exp = tos_date_str(expiration)
    return f"BUY +{quantity} VERTICAL {symbol} 100{wk} {exp} {int(short_strike)}/{int(long_strike)} {option_type} @{limit_price:.2f} LMT"
