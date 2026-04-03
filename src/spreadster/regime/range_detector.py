import numpy as np
import pandas as pd
from typing import Optional
from spreadster.utils.math_utils import round2

def add_session_vwap(bars: pd.DataFrame) -> pd.DataFrame:
    df = bars.copy()
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)
    typical = (df["high"] + df["low"] + df["close"]) / 3.0
    pv = typical * df["volume"]
    df["vwap"] = pv.cumsum() / df["volume"].replace(0, np.nan).cumsum()
    return df

def count_vwap_flips(df: pd.DataFrame) -> int:
    side = np.sign(df["close"] - df["vwap"])
    side = side.replace(0, np.nan).ffill().fillna(0)
    flips = int((side != side.shift(1)).sum() - 1)
    return max(flips, 0)

def compute_range_features(bars: pd.DataFrame, expected_move_points: Optional[float] = None, initial_balance_minutes: int = 60) -> dict:
    df = add_session_vwap(bars)
    start = df["datetime"].iloc[0]
    ib_end = start + pd.Timedelta(minutes=initial_balance_minutes)
    ib = df[df["datetime"] < ib_end]
    ib_high = float(ib["high"].max())
    ib_low = float(ib["low"].min())
    ib_range = ib_high - ib_low
    session_high = float(df["high"].max())
    session_low = float(df["low"].min())
    session_range = session_high - session_low
    open_price = float(df["open"].iloc[0])
    close_price = float(df["close"].iloc[-1])
    current_vwap = float(df["vwap"].iloc[-1])
    flips = count_vwap_flips(df)
    if expected_move_points and expected_move_points > 0:
        range_test_pass = session_range <= expected_move_points * 0.85
        range_reference = expected_move_points
        range_reference_name = "expected_move"
    else:
        range_test_pass = session_range <= ib_range * 1.35
        range_reference = ib_range
        range_reference_name = "initial_balance"
    return {
        "df": df,
        "ib_high": round2(ib_high), "ib_low": round2(ib_low), "ib_range": round2(ib_range),
        "session_high": round2(session_high), "session_low": round2(session_low), "session_range": round2(session_range),
        "open_price": round2(open_price), "close_price": round2(close_price), "current_vwap": round2(current_vwap),
        "vwap_flips": flips, "range_test_pass": range_test_pass,
        "range_reference": round2(range_reference), "range_reference_name": range_reference_name,
    }
