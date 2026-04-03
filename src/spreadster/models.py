from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional

@dataclass
class RegimeResult:
    label: str
    confidence: float
    score: int
    bull_score: int
    bear_score: int
    range_score: int
    details: Dict[str, Any]

@dataclass
class GapExpectedMoveSignal:
    label: str
    previous_close: float
    open_price: float
    expected_move: float
    upper_expected_move: float
    lower_expected_move: float
    distance_to_upper_em: float
    distance_to_lower_em: float
    triggered: bool

@dataclass
class TradeCandidate:
    strategy_type: str
    symbol: str
    expiration: str
    short_put: Optional[float] = None
    long_put: Optional[float] = None
    short_call: Optional[float] = None
    long_call: Optional[float] = None
    short_put_delta: Optional[float] = None
    short_call_delta: Optional[float] = None
    estimated_credit: Optional[float] = None
    max_loss: Optional[float] = None
    quantity: int = 1
    probability_of_profit: Optional[float] = None
    brief_explanation: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
