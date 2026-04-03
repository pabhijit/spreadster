from typing import Optional
from spreadster.models import RegimeResult
from spreadster.regime.range_detector import compute_range_features
from spreadster.regime.trend_detector import compute_trend_features
from spreadster.regime.vwap_detector import compute_vwap_signal
from spreadster.utils.math_utils import clamp

def classify_day(bars, expected_move_points: Optional[float] = None) -> RegimeResult:
    range_features = compute_range_features(bars, expected_move_points=expected_move_points)
    df = range_features.pop("df")
    trend_features = compute_trend_features(df)
    vwap_features = compute_vwap_signal(range_features["vwap_flips"], range_features["close_price"], range_features["current_vwap"], range_features["session_range"])
    range_score = int(range_features["range_test_pass"]) + int(trend_features["trend_test_pass"]) + int(vwap_features["vwap_test_pass"])
    bull_score = trend_features["bull_score"]
    bear_score = trend_features["bear_score"]
    if bull_score >= 3 and bear_score <= 1:
        label = "BULL_TREND"; confidence = clamp(0.55 + 0.10 * bull_score - 0.05 * bear_score, 0.0, 0.98)
    elif bear_score >= 3 and bull_score <= 1:
        label = "BEAR_TREND"; confidence = clamp(0.55 + 0.10 * bear_score - 0.05 * bull_score, 0.0, 0.98)
    elif range_score >= 2:
        label = "RANGE"; confidence = clamp(0.55 + 0.10 * range_score, 0.0, 0.98)
    else:
        label = "MIXED"; confidence = 0.50
    return RegimeResult(label=label, confidence=round(confidence,2), score=range_score, bull_score=bull_score, bear_score=bear_score, range_score=range_score, details={**range_features, **trend_features, **vwap_features})
