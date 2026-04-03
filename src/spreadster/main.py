from __future__ import annotations
import argparse, json, yaml
from pathlib import Path
from spreadster.pipelines.data_pipeline import load_market_context
from spreadster.pipelines.signal_pipeline import run_signal_pipeline
from spreadster.pipelines.report_pipeline import build_final_output
from spreadster.ai.prompts import build_summary_prompt
from spreadster.ai.openai_client import OpenAISummarizer
from spreadster.alerts.telegram_alert import send_telegram_message

def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text())

def main():
    parser = argparse.ArgumentParser(description="spreadster daily options decision engine")
    parser.add_argument("--symbol", default="SPX")
    parser.add_argument("--sample", action="store_true")
    parser.add_argument("--with-openai", action="store_true")
    parser.add_argument("--with-telegram", action="store_true")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    settings = load_yaml(project_root / "config" / "settings.yaml")
    symbols = load_yaml(project_root / "config" / "symbols.yaml")

    symbol = args.symbol.upper()
    width = float(symbols[symbol]["default_wing_width"])
    target_delta = float(settings["default_target_delta"])

    ctx = load_market_context(symbol=symbol, sample=args.sample or settings.get("sample_mode", True))
    regime, gap_signal, recommended_strategy, reason, candidates = run_signal_pipeline(
        symbol=symbol, bars=ctx["bars"], previous_close=ctx["previous_close"], open_price=ctx["open_price"],
        expected_move=ctx["expected_move"], chain=ctx["chain"], expiration=ctx["expiration"], width=width, target_delta=target_delta
    )
    final_output = build_final_output(
        symbol=symbol, spot=ctx["spot"], regime=regime, gap_signal=gap_signal,
        recommended_strategy=recommended_strategy, reason=reason, candidates=candidates
    )
    print(json.dumps(final_output, indent=2))
    final_message = json.dumps(final_output, indent=2)

    if args.with_openai:
        prompt = build_summary_prompt(final_output)
        summarizer = OpenAISummarizer()
        response = summarizer.summarize(prompt)
        print("\nOPENAI SUMMARY RESPONSE\n")
        if "output_text" in response:
            print(response["output_text"])
            final_message = response["output_text"]
        else:
            print(json.dumps(response, indent=2))

    if args.with_telegram:
        sent = send_telegram_message(final_message)
        print(f"\nTELEGRAM SENT: {sent}")

if __name__ == "__main__":
    main()
