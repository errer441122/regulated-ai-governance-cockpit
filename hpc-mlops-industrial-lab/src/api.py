from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
PIPELINE_PATH = BASE_DIR / "src" / "run_pipeline.py"
SPEC = importlib.util.spec_from_file_location("industrial_pipeline_runtime", PIPELINE_PATH)
pipeline = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = pipeline
SPEC.loader.exec_module(pipeline)

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except ImportError:  # pragma: no cover - tests use plain functions without FastAPI
    FastAPI = None
    BaseModel = object


class TelemetryPayload(BaseModel):
    topic: str
    asset_id: str
    timestamp_utc: str
    temperature_c: float
    vibration_mm_s: float
    cycle_time_ms: int
    quality_flag: str


def score_telemetry_payload(payload: dict[str, Any]) -> dict[str, Any]:
    schema_validation = pipeline.validate_industrial_message(payload)
    anomaly_score = pipeline.industrial_anomaly_score(payload) if schema_validation["valid"] else 0.0
    return {
        "asset_id": payload.get("asset_id", ""),
        "schema_validation": schema_validation,
        "anomaly_score": anomaly_score,
        "alert": int(anomaly_score >= 0.5),
        "decision_boundary": "maintenance triage only; no automated shutdown",
    }


if FastAPI:
    app = FastAPI(title="Industrial AI Telemetry Demo API", version="1.0.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": "industrial-telemetry-demo"}

    @app.post("/telemetry/anomaly")
    def score_telemetry(payload: TelemetryPayload) -> dict[str, Any]:
        return score_telemetry_payload(payload.model_dump())
else:
    app = None
