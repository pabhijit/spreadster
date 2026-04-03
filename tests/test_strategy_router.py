from spreadster.models import GapExpectedMoveSignal, RegimeResult
from spreadster.selector.strategy_router import route_strategy

def test_gap_signal_overrides_regime():
    regime = RegimeResult(label="RANGE", confidence=0.8, score=3, bull_score=1, bear_score=1, range_score=3, details={})
    gap = GapExpectedMoveSignal(label="GAP_DOWN_NEAR_LOWER_EM", previous_close=100, open_price=95, expected_move=5, upper_expected_move=105, lower_expected_move=95, distance_to_upper_em=10, distance_to_lower_em=0, triggered=True)
    strategy, _ = route_strategy(regime, gap)
    assert strategy == "PUT_CREDIT_SPREAD"
