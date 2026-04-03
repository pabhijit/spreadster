from __future__ import annotations
import json
from pathlib import Path
from spreadster.live.models import MarketState

def load_market_state(path: str) -> MarketState:
    payload = json.loads(Path(path).read_text())
    return MarketState.model_validate(payload)
