from __future__ import annotations
import json
from openai import OpenAI
from spreadster.config import Config

def build_summary_prompt(payload: dict, concise: bool = True) -> str:
    style = "Be concise." if concise else "Be detailed."
    return (
        "You are an options trading assistant. "
        "Use tested/untested side logic when relevant. "
        f"{style} "
        "Respond ONLY as JSON with keys: action_summary, top_priority, tos_code, rationale.\n\n"
        f"Payload:\n{json.dumps(payload, indent=2)}"
    )

def call_openai(prompt: str, model: str | None = None) -> dict:
    if not Config.OPENAI_ENABLED:
        return {"status": "skipped", "reason": "OPENAI_ENABLED is false"}
    if not Config.OPENAI_API_KEY:
        return {"status": "skipped", "reason": "OPENAI_API_KEY not set"}

    selected_model = model or Config.OPENAI_MODEL
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    try:
        response = client.responses.create(model=selected_model, input=prompt)
        return {"status": "ok", "model": selected_model, "output_text": response.output_text}
    except Exception as e:
        msg = str(e)
        if "insufficient_quota" in msg or "429" in msg:
            return {"status": "error", "model": selected_model, "reason": "OpenAI quota exceeded. Use fallback human summary.", "fallback": True}
        return {"status": "error", "model": selected_model, "reason": msg, "fallback": True}
