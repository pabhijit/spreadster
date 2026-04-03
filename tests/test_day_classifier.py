import pandas as pd
from spreadster.regime.day_classifier import classify_day

def test_classify_day_returns_valid_label():
    bars = pd.DataFrame([
        {"datetime": "2026-03-26T09:30:00", "open": 100, "high": 101, "low": 99.5, "close": 100.5, "volume": 1000},
        {"datetime": "2026-03-26T09:35:00", "open": 100.5, "high": 101.2, "low": 100.1, "close": 100.7, "volume": 1100},
        {"datetime": "2026-03-26T09:40:00", "open": 100.7, "high": 101.0, "low": 100.2, "close": 100.4, "volume": 1050},
        {"datetime": "2026-03-26T09:45:00", "open": 100.4, "high": 100.9, "low": 100.1, "close": 100.6, "volume": 980},
    ])
    result = classify_day(bars, expected_move_points=5)
    assert result.label in {"RANGE", "BULL_TREND", "BEAR_TREND", "MIXED"}
