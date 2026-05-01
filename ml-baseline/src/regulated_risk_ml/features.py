from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import CATEGORICAL_FEATURES, MODEL_FEATURES, NUMERIC_FEATURES, TARGET_COLUMN


@dataclass
class FeatureEngineer:
    """Convert validated CSV records into model-ready dictionaries."""

    numeric_features: list[str] | None = None
    categorical_features: list[str] | None = None

    def __post_init__(self) -> None:
        if self.numeric_features is None:
            self.numeric_features = list(NUMERIC_FEATURES)
        if self.categorical_features is None:
            self.categorical_features = list(CATEGORICAL_FEATURES)

    def transform_record(self, row: dict[str, Any]) -> dict[str, Any]:
        features: dict[str, Any] = {}
        for feature in self.numeric_features or []:
            features[feature] = float(row[feature])
        for feature in self.categorical_features or []:
            features[feature] = str(row[feature])
        return features

    def transform_records(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [self.transform_record(row) for row in rows]

    def labels(self, rows: list[dict[str, Any]]) -> list[int]:
        return [int(row[TARGET_COLUMN]) for row in rows]

    def feature_names(self) -> list[str]:
        return list(MODEL_FEATURES)


def rule_baseline(row: dict[str, Any]) -> int:
    """Transparent conservative fallback for advisory human review triage."""
    return int(
        float(row["data_quality_score"]) < 58
        or float(row["financial_signal_score"]) >= 76
        or float(row["late_payment_signal"]) >= 72
        or float(row["text_risk_score"]) >= 74
        or float(row["sector_risk_score"]) + float(row["region_macro_risk"]) >= 135
    )
