# spreadster

A unified options decision engine with two modes:

- **daily mode** for pre-market / near-open strategy selection
- **live mode** for intraday condor and credit-spread management

This repository preserves the original modular `spreadster` daily package layout and adds a
parallel `live/` package plus shared config, OpenAI, Telegram, and TradingView/Option Omega helpers.

## Package layout

```text
src/spreadster/
├── alerts/
├── ai/
├── config.py
├── formatting/
├── live/
│   ├── ai_alerts.py
│   ├── main.py
│   ├── models.py
│   ├── position_manager.py
│   ├── regime_engine.py
│   ├── state_collector.py
│   └── utils.py
├── pipelines/
├── providers/
├── regime/
├── selector/
├── signals/
├── strategies/
├── utils/
├── cli.py
├── main.py
└── models.py
```

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
```

Run daily sample:

```bash
PYTHONPATH=src python3 -m spreadster.cli daily --sample
```

Run live sample:

```bash
PYTHONPATH=src python3 -m spreadster.cli live --sample
```

Print config:

```bash
PYTHONPATH=src python3 -m spreadster.cli config --print
```

## OpenAI and Telegram

Copy `.env.example` to `.env` and fill in your secrets:

```bash
cp .env.example .env
```

Then you can use:

```bash
PYTHONPATH=src python3 -m spreadster.cli live --sample --with-openai --with-telegram
```

If OpenAI quota is unavailable, live mode falls back to the human summary.

## TradingView + Option Omega flow

1. Run the webhook receiver:
```bash
PYTHONPATH=src python3 scripts/webhook_receiver.py
```

2. Send TradingView alerts to your public webhook URL ending in `/tradingview`

3. Update the Option Omega positions snapshot

4. Merge snapshots:
```bash
PYTHONPATH=src python3 scripts/merge_snapshots.py
```

5. Run live mode:
```bash
PYTHONPATH=src python3 -m spreadster.cli live --input examples/merged_live_state.json --with-telegram
```

## Notes

- `.env` and local snapshots are ignored by `.gitignore`.
- This project is for decision support, not autonomous execution.
- Thinkorswim remains the execution platform; `spreadster` generates TOS order strings and alerts.
