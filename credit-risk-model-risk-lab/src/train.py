from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from data import FEATURE_COLUMNS, split_dataset
from metrics import classification_metrics


BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = BASE_DIR / "artifacts"
REPORT_DIR = BASE_DIR / "reports"
MODEL_PATH = ARTIFACT_DIR / "credit_risk_model.joblib"
TRAINING_SUMMARY_PATH = REPORT_DIR / "training_summary.json"


def candidate_models() -> dict[str, Pipeline]:
    return {
        "logistic_regression_balanced": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        class_weight="balanced",
                        max_iter=1000,
                        n_jobs=1,
                        random_state=42,
                    ),
                ),
            ]
        ),
        "hist_gradient_boosting_probability": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    HistGradientBoostingClassifier(
                        learning_rate=0.06,
                        l2_regularization=0.1,
                        max_iter=90,
                        max_leaf_nodes=31,
                        random_state=42,
                    ),
                ),
            ]
        ),
    }


def train() -> dict[str, object]:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    x_train, x_test, y_train, y_test = split_dataset()

    summaries: dict[str, dict[str, object]] = {}
    fitted_models: dict[str, Pipeline] = {}
    for name, model in candidate_models().items():
        model.fit(x_train, y_train)
        y_score = model.predict_proba(x_test)[:, 1]
        summaries[name] = classification_metrics(y_test, y_score)
        fitted_models[name] = model

    selected_name = max(summaries, key=lambda item: summaries[item]["roc_auc"])
    bundle = {
        "model": fitted_models[selected_name],
        "selected_model": selected_name,
        "feature_columns": FEATURE_COLUMNS,
        "target": "FinancialDistressNextTwoYears",
        "dataset": "OpenML 46929 GiveMeSomeCredit",
        "trained_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "split": {"test_size": 0.2, "random_state": 42, "stratified": True},
    }
    joblib.dump(bundle, MODEL_PATH)

    summary = {
        "dataset": bundle["dataset"],
        "rows": int(len(y_train) + len(y_test)),
        "train_rows": int(len(y_train)),
        "test_rows": int(len(y_test)),
        "event_rate_train": round(float(y_train.mean()), 6),
        "event_rate_test": round(float(y_test.mean()), 6),
        "selected_model": selected_name,
        "model_path": str(MODEL_PATH),
        "candidate_metrics": summaries,
    }
    TRAINING_SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def main() -> None:
    print(json.dumps(train(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
