from spreadster.daily.pipeline import run_daily
from spreadster.live.pipeline import run_live
from pathlib import Path

def test_daily_smoke():
    payload = run_daily(sample=True)
    assert "recommended_strategy" in payload

def test_live_smoke():
    p = Path(__file__).resolve().parents[1] / "examples" / "live_state_example.json"
    payload = run_live(str(p))
    assert payload.regime.label in {"RANGE", "BULL_TREND", "BEAR_TREND", "GAP_DOWN_NEAR_LOWER_EM", "GAP_UP_NEAR_UPPER_EM", "MIXED"}
