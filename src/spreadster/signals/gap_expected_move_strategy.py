from spreadster.models import GapExpectedMoveSignal
from spreadster.utils.math_utils import round2

def detect_gap_expected_move_signal(previous_close: float, open_price: float, expected_move: float, threshold: float = 0.20) -> GapExpectedMoveSignal:
    upper_em = previous_close + expected_move
    lower_em = previous_close - expected_move
    distance_to_upper = abs(open_price - upper_em)
    distance_to_lower = abs(open_price - lower_em)
    near_upper = distance_to_upper <= expected_move * threshold
    near_lower = distance_to_lower <= expected_move * threshold
    if open_price > previous_close and near_upper:
        label = "GAP_UP_NEAR_UPPER_EM"; triggered = True
    elif open_price < previous_close and near_lower:
        label = "GAP_DOWN_NEAR_LOWER_EM"; triggered = True
    else:
        label = "NONE"; triggered = False
    return GapExpectedMoveSignal(label=label, previous_close=round2(previous_close), open_price=round2(open_price), expected_move=round2(expected_move), upper_expected_move=round2(upper_em), lower_expected_move=round2(lower_em), distance_to_upper_em=round2(distance_to_upper), distance_to_lower_em=round2(distance_to_lower), triggered=triggered)
