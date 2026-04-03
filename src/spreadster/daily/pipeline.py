from __future__ import annotations
from datetime import date
import pandas as pd
from spreadster.config import Config
from spreadster.core.models import MarketState, TradeCandidate
from spreadster.core.regime import classify_regime
from spreadster.core.tos import open_code, close_code
from spreadster.core.utils import round2

def build_sample_market_state() -> MarketState:
    return MarketState(
        timestamp_et="2026-04-03 09:40 ET",
        symbol="SPX",
        spot=5703.4,
        vwap=5698.0,
        open_price=5688.1,
        previous_close=5750.25,
        expected_move=60.0,
        initial_balance={"high": 5697.0, "low": 5682.0},
        vwap_flips=0,
        positions=[],
    )

def build_sample_candidates(symbol: str = "SPX") -> list[TradeCandidate]:
    exp = "2026-04-04"
    return [
        TradeCandidate(
            strategy_type="PUT_CREDIT_SPREAD",
            symbol=symbol,
            expiration=exp,
            short_put=5590,
            long_put=5540,
            short_put_delta=-0.20,
            estimated_credit=2.80,
            max_loss=47.20,
            quantity=10,
            probability_of_profit=0.80,
            brief_explanation="Gap-down open near lower expected move; favor fading downside with put credit spreads.",
        ),
        TradeCandidate(
            strategy_type="CALL_CREDIT_SPREAD",
            symbol=symbol,
            expiration=exp,
            short_call=5815,
            long_call=5865,
            short_call_delta=0.20,
            estimated_credit=2.50,
            max_loss=47.50,
            quantity=10,
            probability_of_profit=0.80,
            brief_explanation="Gap-up open near upper expected move; favor fading upside with call credit spreads.",
        ),
        TradeCandidate(
            strategy_type="IRON_CONDOR",
            symbol=symbol,
            expiration=exp,
            short_put=5590,
            long_put=5540,
            short_call=5815,
            long_call=5865,
            short_put_delta=-0.20,
            short_call_delta=0.20,
            estimated_credit=5.30,
            max_loss=44.70,
            quantity=1,
            probability_of_profit=0.69,
            brief_explanation="Neutral premium sale for a range day.",
        ),
    ]

def route_strategy(regime_label: str) -> tuple[str, str]:
    if regime_label == "GAP_DOWN_NEAR_LOWER_EM":
        return "PUT_CREDIT_SPREAD", "Gap-down open near lower expected move; favor fading downside with put credit spreads."
    if regime_label == "GAP_UP_NEAR_UPPER_EM":
        return "CALL_CREDIT_SPREAD", "Gap-up open near upper expected move; favor fading upside with call credit spreads."
    if regime_label == "RANGE":
        return "IRON_CONDOR", "Range day with contained movement and VWAP rotation; favor neutral premium selling."
    if regime_label == "BULL_TREND":
        return "PUT_CREDIT_SPREAD", "Bull trend with defined risk; prefer put credit spreads."
    if regime_label == "BEAR_TREND":
        return "CALL_CREDIT_SPREAD", "Bear trend with defined risk; prefer call credit spreads."
    return "NO_TRADE", "Signals are mixed; no clear edge."

def run_daily(sample: bool = True) -> dict:
    state = build_sample_market_state()
    regime = classify_regime(state, gap_near_em_threshold=Config.GAP_NEAR_EM_THRESHOLD)
    recommended_strategy, reason = route_strategy(regime.label)
    candidates = [c for c in build_sample_candidates(state.symbol) if c.strategy_type == recommended_strategy]

    trade_candidates = []
    for c in candidates:
        item = c.model_dump()
        item["tos_code_open"] = open_code(c, weeklys=Config.USE_WEEKLYS)
        if c.quantity >= 10 and c.strategy_type in {"PUT_CREDIT_SPREAD", "CALL_CREDIT_SPREAD"}:
            item["tos_code_close_30"] = close_code(c, 0.30, quantity=5, weeklys=Config.USE_WEEKLYS)
            item["tos_code_close_50"] = close_code(c, 0.50, quantity=5, weeklys=Config.USE_WEEKLYS)
        else:
            item["tos_code_close_30"] = close_code(c, 0.30, weeklys=Config.USE_WEEKLYS)
            item["tos_code_close_50"] = close_code(c, 0.50, weeklys=Config.USE_WEEKLYS)
        trade_candidates.append(item)

    return {
        "run_date": str(date.today()),
        "symbol": state.symbol,
        "spot_price": round2(state.spot),
        "market_regime": {"label": regime.label, "confidence": regime.confidence, "signals": regime.rationale},
        "gap_signal": {"label": regime.label if regime.label.startswith("GAP_") else "NONE"},
        "recommended_strategy": {"strategy_type": recommended_strategy, "reason": reason},
        "trade_candidates": trade_candidates,
        "openai_summary_input": {"max_words": 120, "style": "concise trader note"},
    }
