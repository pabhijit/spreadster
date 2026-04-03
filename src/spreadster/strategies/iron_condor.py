import pandas as pd
from spreadster.models import TradeCandidate
from spreadster.strategies.common import nearest_short_put, nearest_short_call, option_mid

def build_iron_condor(symbol, chain, expiration, target_delta: float = 0.20, width: float = 50.0, quantity: int = 1):
    sp = nearest_short_put(chain, expiration, target_delta)
    sc = nearest_short_call(chain, expiration, target_delta)
    long_put_strike = float(sp["strike"]) - width
    long_call_strike = float(sc["strike"]) + width
    lp = chain[(chain["expiration"].astype(str) == str(expiration)) & (chain["option_type"] == "PUT") & (pd.to_numeric(chain["strike"], errors="coerce") == long_put_strike)].iloc[0]
    lc = chain[(chain["expiration"].astype(str) == str(expiration)) & (chain["option_type"] == "CALL") & (pd.to_numeric(chain["strike"], errors="coerce") == long_call_strike)].iloc[0]
    credit = (option_mid(sp) - option_mid(lp)) + (option_mid(sc) - option_mid(lc))
    avg_pop = 1.0 - ((abs(float(sp["delta"])) + abs(float(sc["delta"]))) / 2.0)
    return TradeCandidate(strategy_type="IRON_CONDOR", symbol=symbol, expiration=expiration, short_put=float(sp["strike"]), long_put=long_put_strike, short_call=float(sc["strike"]), long_call=long_call_strike, short_put_delta=float(sp["delta"]), short_call_delta=float(sc["delta"]), estimated_credit=round(credit,2), max_loss=round(width - credit,2), probability_of_profit=round(avg_pop,2), quantity=quantity, brief_explanation="Neutral trade that benefits if price stays between the short strikes.")
