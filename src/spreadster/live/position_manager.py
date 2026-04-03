from __future__ import annotations
from typing import List
from spreadster.live.models import MarketState, CondorPosition, SideAssessment, RegimeAssessment
from spreadster.live.utils import pct_profit, side_close_code

def assess_position(state: MarketState, position: CondorPosition, regime: RegimeAssessment, safe_side_profit_take_pct: float = 0.70, tested_side_stop_multiple: float = 1.95, weeklys: bool = True) -> SideAssessment:
    spot = state.spot
    call_distance = position.call_side.short_strike - spot
    put_distance = spot - position.put_side.short_strike
    call_profit_pct = pct_profit(position.call_side.entry_credit, position.call_side.current_value)
    put_profit_pct = pct_profit(position.put_side.entry_credit, position.put_side.current_value)

    if call_distance < put_distance:
        tested_side, untested_side = "CALL", "PUT"
    elif put_distance < call_distance:
        tested_side, untested_side = "PUT", "CALL"
    else:
        tested_side, untested_side = "NONE", "NONE"

    actions: List[str] = []
    tos_codes: List[str] = []

    if untested_side == "PUT" and put_profit_pct >= safe_side_profit_take_pct:
        actions.append(f"Close untested PUT side on {position.id}; profit capture is {put_profit_pct:.1%}.")
        tos_codes.append(side_close_code(position.symbol, position.expiration, "PUT", position.put_side.short_strike, position.put_side.long_strike, position.quantity, position.put_side.current_value, weeklys))

    if untested_side == "CALL" and call_profit_pct >= safe_side_profit_take_pct:
        actions.append(f"Close untested CALL side on {position.id}; profit capture is {call_profit_pct:.1%}.")
        tos_codes.append(side_close_code(position.symbol, position.expiration, "CALL", position.call_side.short_strike, position.call_side.long_strike, position.quantity, position.call_side.current_value, weeklys))

    if tested_side == "CALL" and position.call_side.current_value >= position.call_side.entry_credit * tested_side_stop_multiple:
        actions.append(f"CALL side on {position.id} has hit stop multiple; stop or re-center.")
        tos_codes.append(side_close_code(position.symbol, position.expiration, "CALL", position.call_side.short_strike, position.call_side.long_strike, position.quantity, position.call_side.current_value, weeklys))

    if tested_side == "PUT" and position.put_side.current_value >= position.put_side.entry_credit * tested_side_stop_multiple:
        actions.append(f"PUT side on {position.id} has hit stop multiple; stop or re-center.")
        tos_codes.append(side_close_code(position.symbol, position.expiration, "PUT", position.put_side.short_strike, position.put_side.long_strike, position.quantity, position.put_side.current_value, weeklys))

    if regime.label in {"BULL_TREND", "BEAR_TREND"}:
        actions.append("This is not a balanced condor regime; manage sides independently.")

    if not actions:
        actions.append(f"Hold {position.id} for now; no trigger hit.")

    return SideAssessment(
        position_id=position.id,
        tested_side=tested_side,
        untested_side=untested_side,
        call_profit_pct=call_profit_pct,
        put_profit_pct=put_profit_pct,
        call_distance_to_short=round(call_distance, 2),
        put_distance_to_short=round(put_distance, 2),
        suggested_actions=actions,
        tos_codes=tos_codes,
    )

def assess_all_positions(state: MarketState, regime: RegimeAssessment, safe_side_profit_take_pct: float = 0.70, tested_side_stop_multiple: float = 1.95, weeklys: bool = True):
    return [assess_position(state, p, regime, safe_side_profit_take_pct, tested_side_stop_multiple, weeklys) for p in state.positions]
