from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import CATEGORICAL_FEATURES, NUMERIC_FEATURES, REQUIRED_COLUMNS


def _psi(expected: list[float], actual: list[float], buckets: int = 10) -> float:
    low = min(expected + actual)
    high = max(expected + actual)
    if high == low:
        return 0.0
    width = (high - low) / buckets
    score = 0.0
    for index in range(buckets):
        start = low + index * width
        end = start + width
        exp_count = sum(1 for value in expected if start <= value < end or (index == buckets - 1 and value == high))
        act_count = sum(1 for value in actual if start <= value < end or (index == buckets - 1 and value == high))
        exp_pct = max(exp_count / len(expected), 0.001)
        act_pct = max(act_count / len(actual), 0.001)
        score += (act_pct - exp_pct) * __import__("math").log(act_pct / exp_pct)
    return round(score, 4)


@dataclass
class DriftAnalyzer:
    def data_quality(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        missing_rates = {}
        for column in REQUIRED_COLUMNS:
            missing = sum(1 for row in rows if row.get(column) in (None, ""))
            missing_rates[column] = round(missing / len(rows), 4)
        return {
            "rows": len(rows),
            "required_columns_present": sorted(REQUIRED_COLUMNS),
            "missing_rate_by_column": missing_rates,
            "schema_valid": all(column in rows[0] for column in REQUIRED_COLUMNS),
        }

    def compare(self, train_rows: list[dict[str, Any]], test_rows: list[dict[str, Any]]) -> dict[str, Any]:
        numeric = {}
        for feature in NUMERIC_FEATURES:
            numeric[feature] = {
                "psi_like": _psi(
                    [float(row[feature]) for row in train_rows],
                    [float(row[feature]) for row in test_rows],
                )
            }
        categorical = {}
        for feature in CATEGORICAL_FEATURES:
            train_values = {row[feature] for row in train_rows}
            test_values = {row[feature] for row in test_rows}
            categorical[feature] = {
                "train_unique": len(train_values),
                "test_unique": len(test_values),
                "new_categories_in_test": sorted(test_values - train_values),
            }
        return {
            "data_quality": self.data_quality(train_rows + test_rows),
            "numeric_drift": numeric,
            "categorical_drift": categorical,
            "interpretation": "PSI-like values are local simulation checks, not production drift monitoring.",
        }
