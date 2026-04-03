#!/bin/bash
set -e
PYTHONPATH=src python3 scripts/merge_snapshots.py
PYTHONPATH=src python3 -m spreadster.cli live --input examples/merged_live_state.json --with-telegram
