# spreadster

Unified options decision engine with:
- **daily mode** for strategy selection and candidate generation
- **live mode** for intraday condor/credit-spread management
- shared configuration, AI, Telegram, and webhook integrations

## Modes

### Daily mode
Use this before or near the open to decide whether conditions favor:
- cash-secured puts
- put credit spreads
- call credit spreads
- iron condors

Daily mode combines:
- market regime classification
- gap-to-expected-move logic
- strategy routing
- Thinkorswim order string generation
- optional OpenAI summary

### Live mode
Use this during the session to manage open positions:
- classify regime
- identify tested vs untested side
- detect safe-side profit capture
- detect tested-side stop conditions
- generate Thinkorswim close codes
- optionally send Telegram alerts

## High-level architecture

```text
spreadster/
├── config.py                  # central Config class
├── cli.py                     # unified entrypoint
├── core/                      # shared models, regime, formatting
├── daily/                     # daily decision pipeline
├── live/                      # live monitoring + management
├── integrations/
│   ├── ai/                    # OpenAI support
│   ├── alerts/                # Telegram
│   ├── inputs/                # TradingView / Option Omega / sample loaders
│   └── providers/             # future market data providers
├── scripts/                   # helpers like merge_snapshots and webhook receiver
└── examples/                  # sample payloads
```

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
```

## Run daily mode (sample)

```bash
PYTHONPATH=src python3 -m spreadster.cli daily --sample
```

## Run live mode (sample)

```bash
PYTHONPATH=src python3 -m spreadster.cli live --sample
```

## OpenAI / Telegram

Configure `.env` from `.env.example`, then:

```bash
PYTHONPATH=src python3 -m spreadster.cli live --sample --with-openai --with-telegram
```

## TradingView webhook flow

1. Run the webhook receiver:
```bash
PYTHONPATH=src python3 scripts/webhook_receiver.py
```

2. Send TradingView alerts to your public tunnel URL:
```text
https://your-public-url/tradingview
```

3. Merge TradingView + Option Omega snapshots:
```bash
PYTHONPATH=src python3 scripts/merge_snapshots.py
```

4. Run live mode on the merged file:
```bash
PYTHONPATH=src python3 -m spreadster.cli live --input examples/merged_live_state.json --with-telegram
```

## Notes

- `.env` is intentionally excluded from version control.
- This repo is for **decision support**, not autonomous execution.
- Thinkorswim remains the execution platform; `spreadster` generates TOS order strings and alerts.
