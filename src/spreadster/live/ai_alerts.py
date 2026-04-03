from __future__ import annotations
import json
import requests
from spreadster.config import Config
from spreadster.ai.openai_client import OpenAISummarizer
from spreadster.live.models import DecisionPayload

def build_summary_payload(payload: DecisionPayload) -> dict:
    return {
        "time": payload.market_state.timestamp_et,
        "symbol": payload.market_state.symbol,
        "spot": payload.market_state.spot,
        "vwap": payload.market_state.vwap,
        "regime": payload.regime.model_dump(),
        "positions": [p.model_dump() for p in payload.position_assessments],
        "instruction": "Return the most important action right now and the most important TOS code using concise trader language."
    }

def build_prompt(summary_payload: dict) -> str:
    return "You are an options trading assistant. Use tested/untested side logic. Be concise. Respond ONLY as JSON with keys: action_summary, top_priority, tos_code, rationale.\n\nPayload:\n" + json.dumps(summary_payload, indent=2)

def call_openai(prompt: str, model: str = None) -> dict:
    summarizer = OpenAISummarizer(model=model)
    return summarizer.summarize(prompt)

def send_telegram(message: str) -> bool:
    from spreadster.alerts.telegram_alert import send_telegram_message
    return send_telegram_message(message)
