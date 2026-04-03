from pathlib import Path
import json
import pandas as pd

class SampleProvider:
    def __init__(self, sample_path: str):
        self.payload = json.loads(Path(sample_path).read_text())
    def get_intraday_bars(self, symbol: str) -> pd.DataFrame:
        return pd.DataFrame(self.payload["bars"])
    def get_previous_close(self, symbol: str) -> float:
        return float(self.payload["previous_close"])
    def get_open_price(self, symbol: str) -> float:
        return float(self.payload["open_price"])
    def get_spot_price(self, symbol: str) -> float:
        return float(self.payload["spot_price"])
    def get_option_chain(self, symbol: str) -> pd.DataFrame:
        return pd.DataFrame(self.payload["chain"])
    def get_expected_move(self, symbol: str, expiration: str, spot: float, chain: pd.DataFrame) -> float:
        expiry_df = chain[chain["expiration"].astype(str) == str(expiration)].copy()
        expiry_df["strike"] = pd.to_numeric(expiry_df["strike"], errors="coerce")
        strikes = expiry_df["strike"].dropna().drop_duplicates().sort_values().reset_index(drop=True)
        atm_strike = float(strikes.iloc[(strikes - float(spot)).abs().argmin()])
        calls = expiry_df[(expiry_df["option_type"] == "CALL") & (expiry_df["strike"] == atm_strike)]
        puts = expiry_df[(expiry_df["option_type"] == "PUT") & (expiry_df["strike"] == atm_strike)]
        call_mid = float((calls["bid"].iloc[0] + calls["ask"].iloc[0]) / 2.0)
        put_mid = float((puts["bid"].iloc[0] + puts["ask"].iloc[0]) / 2.0)
        return call_mid + put_mid
