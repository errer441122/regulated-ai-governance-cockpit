from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]


def _load_pipeline_module():
    pipeline_path = BASE_DIR / "src" / "pipeline.py"
    spec = importlib.util.spec_from_file_location("production_capacity_pipeline", pipeline_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load production simulation pipeline.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_ml_model_adapter_module():
    adapter_path = BASE_DIR / "src" / "ml_model_adapter.py"
    spec = importlib.util.spec_from_file_location("production_ml_model_adapter", adapter_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load production ML model adapter.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


pipeline = _load_pipeline_module()
ml_model_adapter = _load_ml_model_adapter_module()

API_VERSION = "1.1.0"
SERVICE_NAME = "regulated-ai-governance-api"
DECISION_BOUNDARY = "advisory human-review triage only"

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except ImportError:  # pragma: no cover - local tests do not require FastAPI
    FastAPI = None
    BaseModel = object


class CapacitySupportRequest(BaseModel):
    programme_id: str
    country: str
    iso3: str
    year: int
    region: str
    internet_users_pct: float
    mobile_subscriptions_per_100: float
    gov_effectiveness_score: float
    disaster_risk_index: float
    fragility_flag: int
    data_protection_maturity: int
    ai_readiness_score: float
    case_notes: str
    needs_capacity_support: int = 0


class RegulatedWorkflowRequest(BaseModel):
    workflow_id: str
    sector: str
    region: str
    lat: float
    lon: float
    data_quality_score: float
    governance_maturity: float
    automation_complexity: float
    stage_age_days: float
    gdpr_sensitive: int
    field_failure_signals: float
    case_notes: str


def score_payload(payload: dict[str, Any]) -> dict[str, Any]:
    probability = pipeline.score_record(payload)
    return {
        "programme_id": payload["programme_id"],
        "country": payload["country"],
        "predicted_capacity_support_probability": probability,
        "predicted_capacity_support": int(probability >= pipeline.CAPACITY_SUPPORT_THRESHOLD),
        "decision_boundary": DECISION_BOUNDARY,
    }


def score_regulated_workflow_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = {key: str(value) for key, value in payload.items()}
    return ml_model_adapter.score_regulated_workflow(normalized)


def metadata_payload() -> dict[str, Any]:
    return {
        "service": SERVICE_NAME,
        "version": API_VERSION,
        "runtime": "FastAPI-compatible Docker service",
        "project_scope": "portfolio production-simulation evidence",
        "decision_boundary": DECISION_BOUNDARY,
        "model_artifact": ml_model_adapter.model_artifact_status(),
        "endpoints": [
            {"method": "GET", "path": "/health", "purpose": "liveness check"},
            {"method": "GET", "path": "/metadata", "purpose": "service scope and model boundary"},
            {"method": "POST", "path": "/score", "purpose": "regulated workflow scoring alias"},
            {"method": "POST", "path": "/score/regulated-workflow", "purpose": "regulated workflow scoring"},
            {"method": "POST", "path": "/score/capacity-support", "purpose": "public-sector capacity-support scoring"},
        ],
        "limitations": [
            "not a production system",
            "not a legal compliance tool",
            "not a credit model",
            "not an automated eligibility or aid-allocation decision system",
            "deployed container may use the transparent fallback if the optional model artifact is absent",
        ],
    }


if FastAPI:
    app = FastAPI(title="Portfolio Production Simulation API", version=API_VERSION)

    @app.get("/")
    def root() -> dict[str, str]:
        return {
            "service": SERVICE_NAME,
            "status": "ok",
            "docs": "/docs",
            "metadata": "/metadata",
        }

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/metadata")
    def metadata() -> dict[str, Any]:
        return metadata_payload()

    @app.post("/score")
    def score(payload: RegulatedWorkflowRequest) -> dict[str, Any]:
        return score_regulated_workflow_payload(payload.model_dump())

    @app.post("/score/capacity-support")
    def score_capacity_support(payload: CapacitySupportRequest) -> dict[str, Any]:
        return score_payload(payload.model_dump())

    @app.post("/score/regulated-workflow")
    def score_regulated_workflow(payload: RegulatedWorkflowRequest) -> dict[str, Any]:
        return score_regulated_workflow_payload(payload.model_dump())
else:
    app = None
