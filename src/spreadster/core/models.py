from __future__ import annotations
from typing import Literal, List, Optional, Dict, Any
from pydantic import BaseModel, Field

class InitialBalance(BaseModel):
    high: float
    low: float

class PositionSide(BaseModel):
    short_strike: float
    long_strike: float
    option_type: Literal["CALL", "PUT"]
    entry_credit: float
    current_value: float

class CondorPosition(BaseModel):
    id: str
    symbol: str = "SPX"
    expiration: str
    quantity: int = 1
    entry_time_et: str
    call_side: PositionSide
    put_side: PositionSide

class MarketState(BaseModel):
    timestamp_et: str
    symbol: str = "SPX"
    spot: float
    vwap: float
    open_price: float
    previous_close: float
    expected_move: float
    initial_balance: InitialBalance
    vwap_flips: int = 0
    positions: List[CondorPosition] = Field(default_factory=list)

class SideAssessment(BaseModel):
    position_id: str
    tested_side: Literal["CALL", "PUT", "NONE"]
    untested_side: Literal["CALL", "PUT", "NONE"]
    call_profit_pct: float
    put_profit_pct: float
    call_distance_to_short: float
    put_distance_to_short: float
    suggested_actions: List[str]
    tos_codes: List[str]

class RegimeAssessment(BaseModel):
    label: Literal["RANGE", "BULL_TREND", "BEAR_TREND", "GAP_DOWN_NEAR_LOWER_EM", "GAP_UP_NEAR_UPPER_EM", "MIXED"]
    confidence: float
    rationale: List[str]

class TradeCandidate(BaseModel):
    strategy_type: Literal["CASH_SECURED_PUT", "PUT_CREDIT_SPREAD", "CALL_CREDIT_SPREAD", "IRON_CONDOR"]
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
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DecisionPayload(BaseModel):
    market_state: MarketState
    regime: RegimeAssessment
    position_assessments: List[SideAssessment]
    summary_for_ai: dict

class DailyDecisionPayload(BaseModel):
    run_date: str
    symbol: str
    spot_price: float
    market_regime: Dict[str, Any]
    gap_signal: Dict[str, Any]
    recommended_strategy: Dict[str, Any]
    trade_candidates: List[Dict[str, Any]]
    openai_summary_input: Dict[str, Any]
