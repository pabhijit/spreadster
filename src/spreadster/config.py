from __future__ import annotations
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_NAME: str = os.getenv("APP_NAME", "spreadster")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    TIMEZONE: str = os.getenv("TIMEZONE", "America/Los_Angeles")
    SYMBOL: str = os.getenv("SYMBOL", "SPX")
    USE_WEEKLYS: bool = os.getenv("USE_WEEKLYS", "true").lower() == "true"

    OPENAI_ENABLED: bool = os.getenv("OPENAI_ENABLED", "false").lower() == "true"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-5")

    TELEGRAM_ENABLED: bool = os.getenv("TELEGRAM_ENABLED", "false").lower() == "true"
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

    OPTION_OMEGA_ENABLED: bool = os.getenv("OPTION_OMEGA_ENABLED", "false").lower() == "true"
    OPTION_OMEGA_API_KEY: str = os.getenv("OPTION_OMEGA_API_KEY", "")
    OPTION_OMEGA_BASE_URL: str = os.getenv("OPTION_OMEGA_BASE_URL", "")
    OPTION_OMEGA_POSITIONS_FILE: str = os.getenv("OPTION_OMEGA_POSITIONS_FILE", "examples/option_omega_positions_example.json")
    OPTION_OMEGA_WEBHOOK_SECRET: str = os.getenv("OPTION_OMEGA_WEBHOOK_SECRET", "")

    TRADINGVIEW_ENABLED: bool = os.getenv("TRADINGVIEW_ENABLED", "false").lower() == "true"
    TRADINGVIEW_WEBHOOK_SECRET: str = os.getenv("TRADINGVIEW_WEBHOOK_SECRET", "")
    TRADINGVIEW_STATE_FILE: str = os.getenv("TRADINGVIEW_STATE_FILE", "examples/tradingview_webhook_example.json")

    LIVE_STATE_FILE: str = os.getenv("LIVE_STATE_FILE", "examples/live_state_example.json")
    MERGED_STATE_FILE: str = os.getenv("MERGED_STATE_FILE", "examples/merged_live_state.json")

    SAFE_SIDE_PROFIT_TAKE_PCT: float = float(os.getenv("SAFE_SIDE_PROFIT_TAKE_PCT", "0.70"))
    SAFE_SIDE_PROFIT_TAKE_PCT_LATE_DAY: float = float(os.getenv("SAFE_SIDE_PROFIT_TAKE_PCT_LATE_DAY", "0.85"))
    TESTED_SIDE_STOP_MULTIPLE: float = float(os.getenv("TESTED_SIDE_STOP_MULTIPLE", "1.95"))
    VWAP_FLIP_THRESHOLD_FOR_RANGE: int = int(os.getenv("VWAP_FLIP_THRESHOLD_FOR_RANGE", "2"))
    TREND_VWAP_PERSISTENCE_MINUTES: int = int(os.getenv("TREND_VWAP_PERSISTENCE_MINUTES", "45"))
    RECENTER_MIN_DISTANCE_POINTS: float = float(os.getenv("RECENTER_MIN_DISTANCE_POINTS", "25"))
    MIN_MINUTES_SINCE_LAST_ENTRY_FOR_RECENTER: int = int(os.getenv("MIN_MINUTES_SINCE_LAST_ENTRY_FOR_RECENTER", "10"))
    ALLOW_REENTRY: bool = os.getenv("ALLOW_REENTRY", "true").lower() == "true"

    DEFAULT_TARGET_DELTA: float = float(os.getenv("DEFAULT_TARGET_DELTA", "0.20"))
    DEFAULT_WING_WIDTH_SPX: float = float(os.getenv("DEFAULT_WING_WIDTH_SPX", "50"))
    DEFAULT_WING_WIDTH_SPY: float = float(os.getenv("DEFAULT_WING_WIDTH_SPY", "5"))
    GAP_NEAR_EM_THRESHOLD: float = float(os.getenv("GAP_NEAR_EM_THRESHOLD", "0.20"))

    @classmethod
    def validate_required_connections(cls) -> Dict[str, bool]:
        return {
            "openai": bool(cls.OPENAI_API_KEY),
            "telegram": bool(cls.TELEGRAM_BOT_TOKEN and cls.TELEGRAM_CHAT_ID),
            "option_omega": bool(cls.OPTION_OMEGA_API_KEY or cls.OPTION_OMEGA_POSITIONS_FILE),
            "tradingview": bool(cls.TRADINGVIEW_WEBHOOK_SECRET or cls.TRADINGVIEW_STATE_FILE),
        }

    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        return {
            k: getattr(cls, k) for k in dir(cls)
            if k.isupper() and not k.startswith("_")
        }

    @classmethod
    def print_status(cls) -> None:
        status = cls.validate_required_connections()
        print("Connection status:")
        for name, ok in status.items():
            print(f"  - {name}: {'configured' if ok else 'missing'}")
