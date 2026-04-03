from __future__ import annotations
import argparse
import json
from pathlib import Path
import yaml

from spreadster.config import Config
from spreadster.live.models import DecisionPayload
from spreadster.live.state_collector import load_market_state
from spreadster.live.regime_engine import classify_regime
from spreadster.live.position_manager import assess_all_positions
from spreadster.live.ai_alerts import build_summary_payload, build_prompt, call_openai, send_telegram

def load_settings() -> dict:
    root = Path(__file__).resolve().parents[2]
    return yaml.safe_load((root / "config" / "settings.yaml").read_text())

def sample_input_path() -> Path:
    return Path(__file__).resolve().parents[2] / "examples" / "live_state_example.json"

def render_human_output(payload: DecisionPayload) -> str:
    lines = []
    lines.append(f"{payload.market_state.timestamp_et} | {payload.market_state.symbol} {payload.market_state.spot}")
    lines.append(f"Regime: {payload.regime.label} ({payload.regime.confidence:.0%})")
    lines.append(f"Reason: {'; '.join(payload.regime.rationale)}")
    for pa in payload.position_assessments:
        lines.append("")
        lines.append(f"{pa.position_id}: tested={pa.tested_side}, untested={pa.untested_side}")
        lines.append(f"  call_profit={pa.call_profit_pct:.1%}, put_profit={pa.put_profit_pct:.1%}")
        for action in pa.suggested_actions:
            lines.append(f"  - {action}")
        for code in pa.tos_codes:
            lines.append(f"  TOS: {code}")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="spreadster live mode")
    parser.add_argument("--sample", action="store_true")
    parser.add_argument("--input")
    parser.add_argument("--with-openai", action="store_true")
    parser.add_argument("--with-telegram", action="store_true")
    args = parser.parse_args()

    settings = load_settings()
    input_path = sample_input_path() if args.sample or not args.input else Path(args.input)

    state = load_market_state(str(input_path))
    regime = classify_regime(state)
    assessments = assess_all_positions(
        state,
        regime,
        safe_side_profit_take_pct=float(settings["safe_side_profit_take_pct"]),
        tested_side_stop_multiple=float(settings["tested_side_stop_multiple"]),
        weeklys=bool(settings["use_weeklys"]),
    )
    payload = DecisionPayload(
        market_state=state,
        regime=regime,
        position_assessments=assessments,
        summary_for_ai={}
    )
    payload.summary_for_ai = build_summary_payload(payload)

    print(json.dumps(payload.model_dump(), indent=2))
    print("\nHUMAN SUMMARY\n")
    human_summary = render_human_output(payload)
    print(human_summary)
    final_message = human_summary

    if args.with_openai:
        response = call_openai(build_prompt(payload.summary_for_ai))
        print("\nOPENAI RESPONSE\n")
        if "output_text" in response:
            print(response["output_text"])
            final_message = response["output_text"]
        else:
            print(json.dumps(response, indent=2))
            print("\nFALLBACK HUMAN SUMMARY\n")
            print(human_summary)
            final_message = human_summary

    if args.with_telegram:
        sent = send_telegram(final_message)
        print(f"\nTELEGRAM SENT: {sent}")

if __name__ == "__main__":
    main()
