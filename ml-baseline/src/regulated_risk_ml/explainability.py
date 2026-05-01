from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from .metrics import ModelEvaluator


@dataclass
class PermutationImportanceExplainer:
    feature_names: list[str]
    random_seed: int = 42

    def explain(
        self,
        model: Any,
        features: list[dict[str, Any]],
        labels: list[int],
    ) -> list[dict[str, float | str]]:
        evaluator = ModelEvaluator()
        baseline = evaluator.evaluate_model(model, features, labels)["f1"]
        rng = random.Random(self.random_seed)
        rows: list[dict[str, float | str]] = []
        for feature in self.feature_names:
            shuffled_values = [row[feature] for row in features]
            rng.shuffle(shuffled_values)
            permuted = [dict(row) for row in features]
            for row, value in zip(permuted, shuffled_values):
                row[feature] = value
            score = evaluator.evaluate_model(model, permuted, labels)["f1"]
            rows.append(
                {
                    "feature": feature,
                    "baseline_f1": round(float(baseline), 4),
                    "permuted_f1": round(float(score), 4),
                    "importance": round(max(0.0, float(baseline) - float(score)), 4),
                    "method": "single-pass permutation on held-out test split",
                }
            )
        return sorted(rows, key=lambda item: float(item["importance"]), reverse=True)
