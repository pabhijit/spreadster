from __future__ import annotations
from spreadster.core.models import TradeCandidate
from spreadster.core.utils import tos_date_str

def side_close_code(symbol: str, expiration: str, option_type: str, short_strike: float, long_strike: float, quantity: int, limit_price: float, weeklys: bool = True) -> str:
    wk = " (Weeklys)" if weeklys else ""
    exp = tos_date_str(expiration)
    return f"BUY +{quantity} VERTICAL {symbol} 100{wk} {exp} {int(short_strike)}/{int(long_strike)} {option_type} @{limit_price:.2f} LMT"

def open_code(candidate: TradeCandidate, weeklys: bool = True) -> str:
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

def close_code(candidate: TradeCandidate, profit_target_pct: float, quantity: int | None = None, weeklys: bool = True) -> str:
    qty = quantity if quantity is not None else candidate.quantity
    buyback = (candidate.estimated_credit or 0.0) * (1 - profit_target_pct)
    if candidate.strategy_type == "CASH_SECURED_PUT":
        exp = tos_date_str(candidate.expiration)
        return f"BUY +{qty} PUT {candidate.symbol} 100 {exp} {int(candidate.short_put)} PUT @{buyback:.2f} LMT"
    if candidate.strategy_type == "PUT_CREDIT_SPREAD":
        return side_close_code(candidate.symbol, candidate.expiration, "PUT", candidate.short_put, candidate.long_put, qty, buyback, weeklys)
    if candidate.strategy_type == "CALL_CREDIT_SPREAD":
        return side_close_code(candidate.symbol, candidate.expiration, "CALL", candidate.short_call, candidate.long_call, qty, buyback, weeklys)
    if candidate.strategy_type == "IRON_CONDOR":
        wk = " (Weeklys)" if weeklys else ""
        exp = tos_date_str(candidate.expiration)
        return f"BUY +{qty} IRON CONDOR {candidate.symbol} 100{wk} {exp} {int(candidate.short_call)}/{int(candidate.long_call)}/{int(candidate.short_put)}/{int(candidate.long_put)} CALL/PUT @{buyback:.2f} LMT"
    raise ValueError(f"Unsupported strategy type: {candidate.strategy_type}")
