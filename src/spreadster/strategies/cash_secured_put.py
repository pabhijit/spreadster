from spreadster.models import TradeCandidate
from spreadster.strategies.common import nearest_short_put, option_mid

def build_cash_secured_put(symbol, chain, expiration, target_delta: float = 0.20, quantity: int = 1):
    sp = nearest_short_put(chain, expiration, target_delta)
    credit = option_mid(sp)
    return TradeCandidate(strategy_type="CASH_SECURED_PUT", symbol=symbol, expiration=expiration, short_put=float(sp["strike"]), short_put_delta=float(sp["delta"]), estimated_credit=round(credit,2), probability_of_profit=round(1.0 - abs(float(sp["delta"])),2), quantity=quantity, brief_explanation="Sell an OTM put and get paid to potentially buy shares lower.")
