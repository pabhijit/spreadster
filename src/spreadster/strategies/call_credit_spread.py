import pandas as pd
from spreadster.models import TradeCandidate
from spreadster.strategies.common import nearest_short_call, option_mid

def build_call_credit_spread(symbol, chain, expiration, target_delta: float = 0.20, width: float = 50.0, quantity: int = 1):
    sc = nearest_short_call(chain, expiration, target_delta)
    long_strike = float(sc["strike"]) + width
    lc = chain[(chain["expiration"].astype(str) == str(expiration)) & (chain["option_type"] == "CALL") & (pd.to_numeric(chain["strike"], errors="coerce") == long_strike)].iloc[0]
    credit = option_mid(sc) - option_mid(lc)
    return TradeCandidate(strategy_type="CALL_CREDIT_SPREAD", symbol=symbol, expiration=expiration, short_call=float(sc["strike"]), long_call=long_strike, short_call_delta=float(sc["delta"]), estimated_credit=round(credit,2), max_loss=round(width - credit,2), probability_of_profit=round(1.0 - abs(float(sc["delta"])),2), quantity=quantity, brief_explanation="Bearish defined-risk premium trade.")
