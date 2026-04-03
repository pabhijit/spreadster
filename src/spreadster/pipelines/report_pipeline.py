from datetime import date
from spreadster.formatting.tos_formatter import open_code, close_code

def build_final_output(symbol, spot, regime, gap_signal, recommended_strategy, reason, candidates):
    trade_candidates = []
    for c in candidates:
        item = c.to_dict()
        item["tos_code_open"] = open_code(c)
        if c.strategy_type in {"PUT_CREDIT_SPREAD", "CALL_CREDIT_SPREAD"} and c.quantity >= 10:
            item["tos_code_close_30"] = close_code(c, 0.30, quantity=5)
            item["tos_code_close_50"] = close_code(c, 0.50, quantity=5)
        else:
            item["tos_code_close_30"] = close_code(c, 0.30)
            item["tos_code_close_50"] = close_code(c, 0.50)
        trade_candidates.append(item)
    return {
        "run_date": str(date.today()),
        "symbol": symbol,
        "spot_price": round(float(spot), 2),
        "market_regime": {"label": regime.label, "confidence": regime.confidence, "signals": regime.details},
        "gap_signal": {"label": gap_signal.label, "triggered": gap_signal.triggered, "previous_close": gap_signal.previous_close, "open_price": gap_signal.open_price, "expected_move": gap_signal.expected_move, "upper_expected_move": gap_signal.upper_expected_move, "lower_expected_move": gap_signal.lower_expected_move, "distance_to_upper_em": gap_signal.distance_to_upper_em, "distance_to_lower_em": gap_signal.distance_to_lower_em},
        "recommended_strategy": {"strategy_type": recommended_strategy, "reason": reason},
        "trade_candidates": trade_candidates,
        "openai_summary_input": {"max_words": 120, "style": "concise trader note"}
    }
