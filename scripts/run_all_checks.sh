#!/usr/bin/env bash
set -euo pipefail

npm test
python -m pytest -q
python ml-baseline/train_model.py
python orchestration/local_orchestrator.py
python scripts/smoke_check.py
