from __future__ import annotations

from typing import Any

from .features import rule_probability


def health() -> dict[str, str]:
    return {"status": "ok", "mode": "local_evidence_simulation"}


def score(payload: dict[str, Any]) -> dict[str, Any]:
    probability = rule_probability(payload)
    return {
        "workflow_id": payload.get("workflow_id", "sample-workflow"),
        "predicted_review_escalation_probability": probability,
        "predicted_review_escalation": int(probability >= 0.5),
        "decision_boundary": "advisory human-review triage only",
    }


def smoke_test() -> dict[str, Any]:
    payload = {
        "workflow_id": "WF-SMOKE-001",
        "sector": "financial_services",
        "region": "EU",
        "data_quality_score": 0.68,
        "governance_maturity": 0.55,
        "automation_complexity": 0.74,
        "stage_age_days": 42,
        "gdpr_sensitive": 1,
        "field_failure_signals": 0.35,
    }
    return {"health": health(), "score": score(payload)}
