from __future__ import annotations
import json
from pathlib import Path
from spreadster.core.models import MarketState

def load_market_state(path: str) -> MarketState:
    payload = json.loads(Path(path).read_text())
    return MarketState.model_validate(payload)

def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text())
