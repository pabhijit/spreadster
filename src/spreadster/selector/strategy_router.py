def route_strategy(regime, gap_signal, willing_to_own_shares: bool = False, want_defined_risk: bool = True):
    if gap_signal.label == "GAP_DOWN_NEAR_LOWER_EM":
        return "PUT_CREDIT_SPREAD", "Gap-down open near lower expected move; favor fading downside with put credit spreads."
    if gap_signal.label == "GAP_UP_NEAR_UPPER_EM":
        return "CALL_CREDIT_SPREAD", "Gap-up open near upper expected move; favor fading upside with call credit spreads."
    if regime.label == "RANGE":
        return "IRON_CONDOR", "Range day with contained movement and VWAP rotation; favor neutral premium selling."
    if regime.label == "BULL_TREND":
        if willing_to_own_shares and not want_defined_risk:
            return "CASH_SECURED_PUT", "Bull trend and assignment-friendly posture; CSP is preferred."
        return "PUT_CREDIT_SPREAD", "Bull trend with defined risk; prefer put credit spreads."
    if regime.label == "BEAR_TREND":
        return "CALL_CREDIT_SPREAD", "Bear trend with defined risk; prefer call credit spreads."
    return "NO_TRADE", "Signals are mixed; no clear edge."
