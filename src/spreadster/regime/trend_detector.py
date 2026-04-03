import numpy as np
from spreadster.utils.math_utils import round2

def compute_trend_features(df, lookback_bars: int = 20) -> dict:
    recent = df.tail(lookback_bars)
    x = np.arange(len(recent))
    slope = np.polyfit(x, recent["close"].values, 1)[0] if len(recent) >= 2 else 0.0
    open_price = float(df["open"].iloc[0])
    close_price = float(df["close"].iloc[-1])
    session_range = max(float(df["high"].max()) - float(df["low"].min()), 1e-9)
    current_vwap = float(df["vwap"].iloc[-1])
    drift = close_price - open_price
    slope_norm = abs(slope) / max(close_price, 1e-9)
    drift_ratio = abs(drift) / session_range
    trend_test_pass = (slope_norm < 0.00035) and (drift_ratio < 0.45)
    bull_score = int(close_price > current_vwap) + int(slope > 0) + int(drift > 0)
    bear_score = int(close_price < current_vwap) + int(slope < 0) + int(drift < 0)
    return {
        "slope_per_bar": round2(float(slope)), "normalized_slope": slope_norm,
        "drift": round2(drift), "drift_ratio": drift_ratio, "trend_test_pass": trend_test_pass,
        "bull_score": bull_score, "bear_score": bear_score,
    }
