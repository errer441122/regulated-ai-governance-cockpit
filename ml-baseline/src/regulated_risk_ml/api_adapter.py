from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import MODEL_ARTIFACT_PATH
from .features import FeatureEngineer, rule_baseline


def normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Map production-sim and direct Risk ML payloads into the trained schema."""
    if "sector_risk_score" in payload:
        return dict(payload)
    data_quality = float(payload.get("data_quality_score", 60))
    governance = float(payload.get("governance_maturity", 3))
    complexity = float(payload.get("automation_complexity", 3))
    stage_age = float(payload.get("stage_age_days", 45))
    gdpr_sensitive = int(float(payload.get("gdpr_sensitive", 0)))
    field_failure = float(payload.get("field_failure_signals", 1))
    note = str(payload.get("case_notes", ""))
    text_risk = min(100.0, 12.0 * len({token.lower().strip(".,;:") for token in note.split()} & {"missing", "complaint", "manual", "override", "dispute", "anomaly", "drift"}))
    return {
        "record_id": payload.get("workflow_id", "API-PAYLOAD"),
        "sector": payload.get("sector", "regulated_workflow"),
        "region": payload.get("region", "unknown"),
        "company_size_bucket": payload.get("company_size_bucket", "mid_market"),
        "company_age_years": float(payload.get("company_age_years", 8)),
        "sector_risk_score": min(100.0, 30.0 + complexity * 9.0 + gdpr_sensitive * 8.0),
        "data_quality_score": data_quality,
        "financial_signal_score": min(100.0, 30.0 + stage_age * 0.45 + field_failure * 7.0),
        "esg_climate_exposure": float(payload.get("esg_climate_exposure", 35)),
        "late_payment_signal": float(payload.get("late_payment_signal", min(100.0, stage_age * 0.8))),
        "region_macro_risk": float(payload.get("region_macro_risk", 35 + max(0.0, 3 - governance) * 12)),
        "text_risk_score": float(payload.get("text_risk_score", text_risk)),
        "geo_distance_risk": float(payload.get("geo_distance_risk", min(100.0, field_failure * 14))),
        "human_review_required": int(data_quality < 65 or governance < 3 or field_failure >= 2),
        "target_default_or_escalation": int(data_quality < 60 or field_failure >= 3),
    }


def _fallback_score(normalized: dict[str, Any]) -> dict[str, Any]:
    prediction = rule_baseline(normalized)
    return {
        "model_source": "transparent_rule_baseline",
        "needs_human_escalation_probability": 0.78 if prediction else 0.22,
        "needs_human_escalation": prediction,
    }


def score_payload(payload: dict[str, Any], model_path: Path = MODEL_ARTIFACT_PATH) -> dict[str, Any]:
    normalized = normalize_payload(payload)
    result: dict[str, Any]
    if model_path.exists():
        try:
            import joblib

            bundle = joblib.load(model_path)
            model = bundle["model"]
            features = FeatureEngineer().transform_records([normalized])
            probability = round(float(model.predict_proba(features)[0][1]), 4)
            result = {
                "model_source": bundle.get("selected_model", "sklearn_artifact"),
                "needs_human_escalation_probability": probability,
                "needs_human_escalation": int(probability >= 0.5),
            }
        except Exception as exc:  # pragma: no cover - defensive fallback for optional artifact loading
            result = _fallback_score(normalized)
            result["model_load_error"] = exc.__class__.__name__
    else:
        result = _fallback_score(normalized)
    return {
        "workflow_id": str(payload.get("workflow_id", normalized.get("record_id", "unknown"))),
        **result,
        "artifact_status": {
            "path": str(model_path),
            "exists": model_path.exists(),
            "fallback": "transparent_rule_baseline",
        },
        "decision_boundary": "advisory human-review triage only",
    }
