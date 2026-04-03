# Walkthrough

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
```

## Daily mode

```bash
PYTHONPATH=src python3 -m spreadster.cli daily --sample
```

Optional:

```bash
PYTHONPATH=src python3 -m spreadster.cli daily --sample --with-openai --with-telegram
```

## Live mode

```bash
PYTHONPATH=src python3 -m spreadster.cli live --sample
```

Optional:

```bash
PYTHONPATH=src python3 -m spreadster.cli live --sample --with-openai --with-telegram
```

## TradingView + Option Omega

1. Run webhook receiver:
```bash
PYTHONPATH=src python3 scripts/webhook_receiver.py
```

2. Update the Option Omega positions file

3. Merge snapshots:
```bash
PYTHONPATH=src python3 scripts/merge_snapshots.py
```

4. Run live mode:
```bash
PYTHONPATH=src python3 -m spreadster.cli live --input examples/merged_live_state.json --with-telegram
```
