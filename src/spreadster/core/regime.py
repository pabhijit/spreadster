from __future__ import annotations
from spreadster.core.models import MarketState, RegimeAssessment

def classify_regime(state: MarketState, gap_near_em_threshold: float = 0.20) -> RegimeAssessment:
    rationale = []
    upper_em = state.previous_close + state.expected_move
    lower_em = state.previous_close - state.expected_move

    if state.open_price > state.previous_close and abs(state.open_price - upper_em) <= gap_near_em_threshold * state.expected_move:
        rationale.append("Open is near upper expected move.")
        return RegimeAssessment(label="GAP_UP_NEAR_UPPER_EM", confidence=0.82, rationale=rationale)

    if state.open_price < state.previous_close and abs(state.open_price - lower_em) <= gap_near_em_threshold * state.expected_move:
        rationale.append("Open is near lower expected move.")
        return RegimeAssessment(label="GAP_DOWN_NEAR_LOWER_EM", confidence=0.82, rationale=rationale)

    if state.vwap_flips >= 2 and state.initial_balance.low <= state.spot <= state.initial_balance.high:
        rationale.append("Multiple VWAP flips and price inside initial balance.")
        return RegimeAssessment(label="RANGE", confidence=0.75, rationale=rationale)

    if state.spot > state.vwap and state.spot > state.initial_balance.high and state.vwap_flips == 0:
        rationale.append("Price above VWAP and above initial balance with no flips.")
        return RegimeAssessment(label="BULL_TREND", confidence=0.84, rationale=rationale)

    if state.spot < state.vwap and state.spot < state.initial_balance.low and state.vwap_flips == 0:
        rationale.append("Price below VWAP and below initial balance with no flips.")
        return RegimeAssessment(label="BEAR_TREND", confidence=0.84, rationale=rationale)

    rationale.append("Signals are mixed.")
    return RegimeAssessment(label="MIXED", confidence=0.55, rationale=rationale)
