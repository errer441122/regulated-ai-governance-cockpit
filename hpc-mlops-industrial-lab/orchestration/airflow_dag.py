"""Illustrative Airflow adapter.

This file is not executed by local CI because Apache Airflow is intentionally
not a dependency of the portfolio repo. It shows how the executable pipeline
would be scheduled in a production-like environment.
"""

from __future__ import annotations

import importlib.util
import sys
from datetime import datetime
from pathlib import Path


try:
    from airflow.decorators import dag, task
except ImportError:  # pragma: no cover - reviewer documentation path
    dag = None
    task = None


if dag and task:

    def _load_pipeline_module():
        pipeline_path = Path(__file__).resolve().parents[1] / "src" / "run_pipeline.py"
        spec = importlib.util.spec_from_file_location("regulated_hpc_pipeline", pipeline_path)
        module = importlib.util.module_from_spec(spec)
        if spec is None or spec.loader is None:
            raise RuntimeError("Could not load regulated AI pipeline module.")
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    @dag(
        dag_id="regulated_ai_risk_lab",
        start_date=datetime(2026, 1, 1),
        schedule="@daily",
        catchup=False,
        tags=["portfolio", "regulated-ai", "mlops"],
    )
    def regulated_ai_risk_lab():
        @task
        def run_training_pipeline() -> str:
            result = _load_pipeline_module().run_pipeline()
            return str(result["artifacts"]["model_card"])

        run_training_pipeline()

    regulated_ai_risk_lab()
