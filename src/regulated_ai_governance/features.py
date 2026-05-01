from __future__ import annotations

from typing import Any


NUMERIC_FEATURES = [
    "data_quality_score",
    "governance_maturity",
    "automation_complexity",
    "stage_age_days",
    "gdpr_sensitive",
    "field_failure_signals",
]


def build_feature_vector(record: dict[str, Any]) -> dict[str, float]:
    """Return the stable numeric feature contract used by smoke tests."""
    vector: dict[str, float] = {}
    for feature in NUMERIC_FEATURES:
        vector[feature] = float(record.get(feature, 0.0))
    vector["risk_pressure"] = (
        (1.0 - vector["data_quality_score"])
        + vector["automation_complexity"]
        + min(vector["stage_age_days"] / 120.0, 1.0)
        + vector["field_failure_signals"]
    )
    return vector


def rule_probability(record: dict[str, Any]) -> float:
    vector = build_feature_vector(record)
    score = (
        0.18
        + 0.22 * (1.0 - vector["data_quality_score"])
        + 0.18 * (1.0 - vector["governance_maturity"])
        + 0.16 * vector["automation_complexity"]
        + 0.12 * min(vector["stage_age_days"] / 120.0, 1.0)
        + 0.08 * vector["gdpr_sensitive"]
        + 0.16 * vector["field_failure_signals"]
    )
    return round(max(0.01, min(score, 0.99)), 4)
