from spreadster.regime.day_classifier import classify_day
from spreadster.signals.gap_expected_move_strategy import detect_gap_expected_move_signal
from spreadster.selector.strategy_router import route_strategy
from spreadster.strategies.cash_secured_put import build_cash_secured_put
from spreadster.strategies.put_credit_spread import build_put_credit_spread
from spreadster.strategies.call_credit_spread import build_call_credit_spread
from spreadster.strategies.iron_condor import build_iron_condor

def build_candidates(symbol, chain, expiration, recommended_strategy, width, target_delta):
    if recommended_strategy == "CASH_SECURED_PUT":
        return [build_cash_secured_put(symbol, chain, expiration, target_delta=target_delta, quantity=1)]
    if recommended_strategy == "PUT_CREDIT_SPREAD":
        return [build_put_credit_spread(symbol, chain, expiration, target_delta=target_delta, width=width, quantity=10)]
    if recommended_strategy == "CALL_CREDIT_SPREAD":
        return [build_call_credit_spread(symbol, chain, expiration, target_delta=target_delta, width=width, quantity=10)]
    if recommended_strategy == "IRON_CONDOR":
        return [build_iron_condor(symbol, chain, expiration, target_delta=target_delta, width=width, quantity=1)]
    return []

def run_signal_pipeline(symbol, bars, previous_close, open_price, expected_move, chain, expiration, width, target_delta):
    regime = classify_day(bars, expected_move_points=expected_move)
    gap_signal = detect_gap_expected_move_signal(previous_close, open_price, expected_move)
    recommended_strategy, reason = route_strategy(regime, gap_signal, willing_to_own_shares=False, want_defined_risk=True)
    candidates = build_candidates(symbol, chain, expiration, recommended_strategy, width=width, target_delta=target_delta)
    return regime, gap_signal, recommended_strategy, reason, candidates
