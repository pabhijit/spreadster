from __future__ import annotations
import argparse
import json
from pathlib import Path

from spreadster.config import Config
from spreadster.daily.pipeline import run_daily
from spreadster.live.pipeline import run_live
from spreadster.integrations.ai import build_summary_prompt, call_openai
from spreadster.integrations.telegram import send_telegram

def sample_live_input_path() -> Path:
    return Path(__file__).resolve().parents[2] / "examples" / "live_state_example.json"

def render_live_human_output(payload) -> str:
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
    parser = argparse.ArgumentParser(description="spreadster unified CLI")
    sub = parser.add_subparsers(dest="mode", required=True)

    p_daily = sub.add_parser("daily")
    p_daily.add_argument("--sample", action="store_true")
    p_daily.add_argument("--with-openai", action="store_true")
    p_daily.add_argument("--with-telegram", action="store_true")

    p_live = sub.add_parser("live")
    p_live.add_argument("--sample", action="store_true")
    p_live.add_argument("--input")
    p_live.add_argument("--with-openai", action="store_true")
    p_live.add_argument("--with-telegram", action="store_true")

    p_cfg = sub.add_parser("config")
    p_cfg.add_argument("--print", action="store_true")

    args = parser.parse_args()

    if args.mode == "config":
        print(json.dumps(Config.as_dict(), indent=2))
        Config.print_status()
        return

    if args.mode == "daily":
        payload = run_daily(sample=args.sample)
        print(json.dumps(payload, indent=2))
        final_message = json.dumps(payload, indent=2)
        if args.with_openai:
            response = call_openai(build_summary_prompt(payload))
            print("\nOPENAI RESPONSE\n")
            if "output_text" in response:
                print(response["output_text"])
                final_message = response["output_text"]
            else:
                print(json.dumps(response, indent=2))
        if args.with_telegram:
            sent = send_telegram(final_message)
            print(f"\nTELEGRAM SENT: {sent}")
        return

    if args.mode == "live":
        input_path = str(sample_live_input_path()) if args.sample or not args.input else args.input
        payload = run_live(input_path)
        print(json.dumps(payload.model_dump(), indent=2))
        print("\nHUMAN SUMMARY\n")
        human_summary = render_live_human_output(payload)
        print(human_summary)
        final_message = human_summary
        if args.with_openai:
            response = call_openai(build_summary_prompt(payload.summary_for_ai))
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
        return

if __name__ == "__main__":
    main()
