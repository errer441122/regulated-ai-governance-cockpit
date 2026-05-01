from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

try:
    from dagster import asset
except ImportError:  # pragma: no cover - Dagster is intentionally optional
    asset = None


def _run(command: list[str]) -> str:
    completed = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
    return completed.stdout


if asset:

    @asset
    def risk_ml_baseline() -> str:
        return _run([sys.executable, "ml-baseline/train_model.py"])

    @asset
    def production_simulation() -> str:
        return _run([sys.executable, "production-sim-stack/src/orchestrate.py"])

    @asset
    def undp_sdg_lab() -> str:
        return _run([sys.executable, "undp-sdg-risk-lab/src/run_pipeline.py"])
