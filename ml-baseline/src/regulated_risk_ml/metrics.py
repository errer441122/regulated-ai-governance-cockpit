from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


@dataclass
class ModelEvaluator:
    threshold: float = 0.5

    def evaluate_probabilities(self, labels: list[int], probabilities: list[float]) -> dict[str, Any]:
        predictions = [1 if probability >= self.threshold else 0 for probability in probabilities]
        matrix = confusion_matrix(labels, predictions).tolist()
        return {
            "roc_auc": round(roc_auc_score(labels, probabilities), 4),
            "pr_auc": round(average_precision_score(labels, probabilities), 4),
            "precision": round(precision_score(labels, predictions, zero_division=0), 4),
            "recall": round(recall_score(labels, predictions, zero_division=0), 4),
            "f1": round(f1_score(labels, predictions, zero_division=0), 4),
            "brier_score": round(brier_score_loss(labels, probabilities), 4),
            "confusion_matrix": matrix,
            "true_negative": matrix[0][0],
            "false_positive": matrix[0][1],
            "false_negative": matrix[1][0],
            "true_positive": matrix[1][1],
        }

    def evaluate_model(self, model: Any, features: list[dict[str, Any]], labels: list[int]) -> dict[str, Any]:
        probabilities = [float(score[1]) for score in model.predict_proba(features)]
        return self.evaluate_probabilities(labels, probabilities)
