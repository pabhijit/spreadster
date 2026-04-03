from pathlib import Path
from spreadster.pipelines.data_pipeline import load_market_context
from spreadster.live.state_collector import load_market_state
from spreadster.live.regime_engine import classify_regime

def test_daily_sample_provider():
    ctx = load_market_context("SPX", sample=True)
    assert "bars" in ctx and "chain" in ctx

def test_live_sample_load():
    p = Path(__file__).resolve().parents[1] / "examples" / "live_state_example.json"
    state = load_market_state(str(p))
    regime = classify_regime(state)
    assert regime.label in {"RANGE", "BULL_TREND", "BEAR_TREND", "GAP_DOWN_NEAR_LOWER_EM", "GAP_UP_NEAR_UPPER_EM", "MIXED"}
