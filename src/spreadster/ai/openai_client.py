from __future__ import annotations
from openai import OpenAI
from spreadster.config import Config

class OpenAISummarizer:
    def __init__(self, model: str = None):
        self.model = model or Config.OPENAI_MODEL

    def summarize(self, prompt: str) -> dict:
        if not Config.OPENAI_ENABLED:
            return {"status": "skipped", "reason": "OPENAI_ENABLED is false"}
        if not Config.OPENAI_API_KEY:
            return {"status": "skipped", "reason": "OPENAI_API_KEY not set"}
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        try:
            response = client.responses.create(model=self.model, input=prompt)
            return {"status": "ok", "model": self.model, "output_text": response.output_text}
        except Exception as e:
            msg = str(e)
            if "insufficient_quota" in msg or "429" in msg:
                return {"status": "error", "model": self.model, "reason": "OpenAI quota exceeded. Use fallback human summary.", "fallback": True}
            return {"status": "error", "model": self.model, "reason": msg, "fallback": True}
