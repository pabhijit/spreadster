import pandas as pd

def nearest_short_put(chain: pd.DataFrame, expiration: str, target_delta: float):
    df = chain[(chain["expiration"].astype(str) == str(expiration)) & (chain["option_type"] == "PUT")].copy()
    df["delta"] = pd.to_numeric(df["delta"], errors="coerce")
    df["strike"] = pd.to_numeric(df["strike"], errors="coerce")
    df["delta_dist"] = (df["delta"].abs() - abs(target_delta)).abs()
    return df.sort_values(["delta_dist", "strike"], ascending=[True, False]).iloc[0]

def nearest_short_call(chain: pd.DataFrame, expiration: str, target_delta: float):
    df = chain[(chain["expiration"].astype(str) == str(expiration)) & (chain["option_type"] == "CALL")].copy()
    df["delta"] = pd.to_numeric(df["delta"], errors="coerce")
    df["strike"] = pd.to_numeric(df["strike"], errors="coerce")
    df["delta_dist"] = (df["delta"] - abs(target_delta)).abs()
    return df.sort_values(["delta_dist", "strike"], ascending=[True, True]).iloc[0]

def option_mid(row):
    return float((float(row["bid"]) + float(row["ask"])) / 2.0)
