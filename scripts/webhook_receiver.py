from __future__ import annotations
import json
from pathlib import Path
from flask import Flask, request, jsonify
from spreadster.config import Config

app = Flask(__name__)

REQUIRED_KEYS = {"symbol", "spot", "vwap", "open_price", "previous_close", "expected_move", "ib_high", "ib_low", "vwap_flips", "timestamp_et"}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "service": "spreadster_tradingview_webhook"}), 200

@app.route("/tradingview", methods=["POST"])
def tradingview():
    try:
        payload = request.get_json(force=True, silent=False)
    except Exception as e:
        return jsonify({"ok": False, "error": f"invalid_json: {e}"}), 400
    if not isinstance(payload, dict):
        return jsonify({"ok": False, "error": "payload must be a JSON object"}), 400

    missing = sorted(REQUIRED_KEYS - set(payload.keys()))
    if missing:
        return jsonify({"ok": False, "error": f"missing_keys: {missing}"}), 400

    secret = request.headers.get("X-Spreadster-Secret", "")
    if Config.TRADINGVIEW_WEBHOOK_SECRET and secret != Config.TRADINGVIEW_WEBHOOK_SECRET:
        return jsonify({"ok": False, "error": "invalid webhook secret"}), 403

    out_path = Path(Config.TRADINGVIEW_STATE_FILE)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2))
    return jsonify({"ok": True, "written_to": str(out_path)}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
