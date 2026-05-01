from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .config import RANDOM_SEED
from .features import rule_baseline


@dataclass
class ModelTrainer:
    random_seed: int = RANDOM_SEED
    test_size: float = 0.3

    def split(
        self,
        features: list[dict[str, Any]],
        labels: list[int],
        rows: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[int], list[int], list[dict[str, Any]], list[dict[str, Any]]]:
        return train_test_split(
            features,
            labels,
            rows,
            test_size=self.test_size,
            random_state=self.random_seed,
            stratify=labels,
        )

    def build_logistic_pipeline(self) -> Pipeline:
        return Pipeline(
            [
                ("features", DictVectorizer(sparse=False)),
                ("scale", StandardScaler()),
                (
                    "model",
                    LogisticRegression(max_iter=1000, class_weight="balanced", random_state=self.random_seed),
                ),
            ]
        )

    def build_random_forest_pipeline(self) -> Pipeline:
        return Pipeline(
            [
                ("features", DictVectorizer(sparse=False)),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=120,
                        min_samples_leaf=4,
                        class_weight="balanced",
                        random_state=self.random_seed,
                    ),
                ),
            ]
        )

    def train_models(self, train_x: list[dict[str, Any]], train_y: list[int]) -> dict[str, Pipeline]:
        models = {
            "logistic_regression": self.build_logistic_pipeline(),
            "random_forest": self.build_random_forest_pipeline(),
        }
        for model in models.values():
            model.fit(train_x, train_y)
        return models

    def rule_predictions(self, rows: list[dict[str, Any]]) -> list[int]:
        return [rule_baseline(row) for row in rows]
