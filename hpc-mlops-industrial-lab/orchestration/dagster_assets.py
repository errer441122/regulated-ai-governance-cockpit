"""Illustrative Dagster asset wrapper for the regulated AI lab.

The local project keeps dependencies minimal. In a real Dagster deployment this
asset would materialize metrics and model-card artifacts into object storage.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


try:
    from dagster import asset
except ImportError:  # pragma: no cover - reviewer documentation path
    asset = None


if asset:

    def _load_pipeline_module():
        pipeline_path = Path(__file__).resolve().parents[1] / "src" / "run_pipeline.py"
        spec = importlib.util.spec_from_file_location("regulated_hpc_pipeline", pipeline_path)
        module = importlib.util.module_from_spec(spec)
        if spec is None or spec.loader is None:
            raise RuntimeError("Could not load regulated AI pipeline module.")
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    @asset(group_name="regulated_ai_portfolio")
    def regulated_ai_model_card() -> str:
        result = _load_pipeline_module().run_pipeline()
        return str(result["artifacts"]["model_card"])
