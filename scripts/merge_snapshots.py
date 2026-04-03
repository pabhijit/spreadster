from __future__ import annotations
import json
from pathlib import Path
from spreadster.config import Config

def main():
    tv_path = Path(Config.TRADINGVIEW_STATE_FILE)
    oo_path = Path(Config.OPTION_OMEGA_POSITIONS_FILE)
    out_path = Path(Config.MERGED_STATE_FILE)

    if not tv_path.exists():
        raise FileNotFoundError(f"TradingView state file not found: {tv_path}")
    if not oo_path.exists():
        raise FileNotFoundError(f"Option Omega positions file not found: {oo_path}")

    tv = json.loads(tv_path.read_text())
    oo = json.loads(oo_path.read_text())

    merged = {
        "timestamp_et": tv["timestamp_et"],
        "symbol": tv.get("symbol", Config.SYMBOL),
        "spot": tv["spot"],
        "vwap": tv["vwap"],
        "open_price": tv["open_price"],
        "previous_close": tv["previous_close"],
        "expected_move": tv["expected_move"],
        "initial_balance": {"high": tv["ib_high"], "low": tv["ib_low"]},
        "vwap_flips": tv.get("vwap_flips", 0),
        "positions": oo["positions"],
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(merged, indent=2))
    print(f"Wrote merged state to {out_path}")

if __name__ == "__main__":
    main()
