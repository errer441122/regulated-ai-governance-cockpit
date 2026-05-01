#!/usr/bin/env bash
set -euo pipefail

echo "Running local production-simulation smoke checks."
python production-sim-stack/src/orchestrate.py
python production-sim-stack/scripts/check_api_contract.py

if command -v docker >/dev/null 2>&1; then
  echo "Docker is available. Optional compose smoke can be run manually from production-sim-stack/."
  echo "This script does not claim real cloud deployment."
else
  echo "Docker not available; skipped optional compose checks."
fi
