from typing import Optional
from spreadster.utils.dates import tos_date_str

def open_code(candidate, weeklys: bool = True) -> str:
    wk = " (Weeklys)" if weeklys else ""
    qty = candidate.quantity
    exp = tos_date_str(candidate.expiration)
    credit = candidate.estimated_credit or 0.0
    if candidate.strategy_type == "CASH_SECURED_PUT":
        return f"SELL -{qty} PUT {candidate.symbol} 100 {exp} {int(candidate.short_put)} PUT @{credit:.2f} LMT"
    if candidate.strategy_type == "PUT_CREDIT_SPREAD":
        return f"SELL -{qty} VERTICAL {candidate.symbol} 100{wk} {exp} {int(candidate.short_put)}/{int(candidate.long_put)} PUT @{credit:.2f} LMT"
    if candidate.strategy_type == "CALL_CREDIT_SPREAD":
        return f"SELL -{qty} VERTICAL {candidate.symbol} 100{wk} {exp} {int(candidate.short_call)}/{int(candidate.long_call)} CALL @{credit:.2f} LMT"
    if candidate.strategy_type == "IRON_CONDOR":
        return f"SELL -{qty} IRON CONDOR {candidate.symbol} 100{wk} {exp} {int(candidate.short_call)}/{int(candidate.long_call)}/{int(candidate.short_put)}/{int(candidate.long_put)} CALL/PUT @{credit:.2f} LMT"
    raise ValueError(f"Unsupported strategy type: {candidate.strategy_type}")

def close_code(candidate, profit_target_pct: float, quantity: Optional[int] = None, weeklys: bool = True) -> str:
    wk = " (Weeklys)" if weeklys else ""
    qty = quantity if quantity is not None else candidate.quantity
    exp = tos_date_str(candidate.expiration)
    buyback = (candidate.estimated_credit or 0.0) * (1 - profit_target_pct)
    if candidate.strategy_type == "CASH_SECURED_PUT":
        return f"BUY +{qty} PUT {candidate.symbol} 100 {exp} {int(candidate.short_put)} PUT @{buyback:.2f} LMT"
    if candidate.strategy_type == "PUT_CREDIT_SPREAD":
        return f"BUY +{qty} VERTICAL {candidate.symbol} 100{wk} {exp} {int(candidate.short_put)}/{int(candidate.long_put)} PUT @{buyback:.2f} LMT"
    if candidate.strategy_type == "CALL_CREDIT_SPREAD":
        return f"BUY +{qty} VERTICAL {candidate.symbol} 100{wk} {exp} {int(candidate.short_call)}/{int(candidate.long_call)} CALL @{buyback:.2f} LMT"
    if candidate.strategy_type == "IRON_CONDOR":
        return f"BUY +{qty} IRON CONDOR {candidate.symbol} 100{wk} {exp} {int(candidate.short_call)}/{int(candidate.long_call)}/{int(candidate.short_put)}/{int(candidate.long_put)} CALL/PUT @{buyback:.2f} LMT"
    raise ValueError(f"Unsupported strategy type: {candidate.strategy_type}")
