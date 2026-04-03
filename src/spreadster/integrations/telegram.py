from __future__ import annotations
import requests
from spreadster.config import Config

def send_telegram(message: str) -> bool:
    if not Config.TELEGRAM_ENABLED:
        return False
    if not Config.TELEGRAM_BOT_TOKEN or not Config.TELEGRAM_CHAT_ID:
        return False
    try:
        url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
        resp = requests.post(url, json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message}, timeout=10)
        return resp.ok
    except Exception:
        return False
