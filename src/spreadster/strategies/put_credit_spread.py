import pandas as pd
from spreadster.models import TradeCandidate
from spreadster.strategies.common import nearest_short_put, option_mid

def build_put_credit_spread(symbol, chain, expiration, target_delta: float = 0.20, width: float = 50.0, quantity: int = 1):
    sp = nearest_short_put(chain, expiration, target_delta)
    long_strike = float(sp["strike"]) - width
    lp = chain[(chain["expiration"].astype(str) == str(expiration)) & (chain["option_type"] == "PUT") & (pd.to_numeric(chain["strike"], errors="coerce") == long_strike)].iloc[0]
    credit = option_mid(sp) - option_mid(lp)
    return TradeCandidate(strategy_type="PUT_CREDIT_SPREAD", symbol=symbol, expiration=expiration, short_put=float(sp["strike"]), long_put=long_strike, short_put_delta=float(sp["delta"]), estimated_credit=round(credit,2), max_loss=round(width - credit,2), probability_of_profit=round(1.0 - abs(float(sp["delta"])),2), quantity=quantity, brief_explanation="Bullish defined-risk premium trade.")
