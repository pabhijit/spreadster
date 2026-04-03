from __future__ import annotations
from spreadster.config import Config
from spreadster.core.models import DecisionPayload
from spreadster.core.regime import classify_regime
from spreadster.integrations.inputs import load_market_state
from spreadster.live.position_manager import assess_all_positions

def build_summary_payload(payload: DecisionPayload) -> dict:
    return {
        "time": payload.market_state.timestamp_et,
        "symbol": payload.market_state.symbol,
        "spot": payload.market_state.spot,
        "vwap": payload.market_state.vwap,
        "regime": payload.regime.model_dump(),
        "positions": [p.model_dump() for p in payload.position_assessments],
        "instruction": "Return the most important action right now and the most important TOS code using concise trader language.",
    }

def run_live(input_path: str) -> DecisionPayload:
    state = load_market_state(input_path)
    regime = classify_regime(state, gap_near_em_threshold=Config.GAP_NEAR_EM_THRESHOLD)
    assessments = assess_all_positions(
        state,
        regime,
        safe_side_profit_take_pct=Config.SAFE_SIDE_PROFIT_TAKE_PCT,
        tested_side_stop_multiple=Config.TESTED_SIDE_STOP_MULTIPLE,
        weeklys=Config.USE_WEEKLYS,
    )
    payload = DecisionPayload(
        market_state=state,
        regime=regime,
        position_assessments=assessments,
        summary_for_ai={},
    )
    payload.summary_for_ai = build_summary_payload(payload)
    return payload
