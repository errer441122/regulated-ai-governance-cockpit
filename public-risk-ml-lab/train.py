from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "wisconsin_breast_cancer_public.csv"
ARTIFACT_DIR = BASE_DIR / "artifacts"


def _load_dataset() -> tuple[list[str], list[list[float]], list[int]]:
    if not DATA_PATH.exists():
        from fetch_or_prepare_data import prepare_data

        prepare_data(DATA_PATH)
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    feature_names = [column for column in rows[0].keys() if column not in {"record_id", "high_risk_label"}]
    x = [[float(row[column]) for column in feature_names] for row in rows]
    y = [int(row["high_risk_label"]) for row in rows]
    return feature_names, x, y


def _metrics(y_true: list[int], probabilities: list[float]) -> dict[str, Any]:
    predictions = [int(probability >= 0.5) for probability in probabilities]
    return {
        "roc_auc": round(float(roc_auc_score(y_true, probabilities)), 4),
        "pr_auc": round(float(average_precision_score(y_true, probabilities)), 4),
        "precision": round(float(precision_score(y_true, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, predictions, zero_division=0)), 4),
        "brier_score": round(float(brier_score_loss(y_true, probabilities)), 4),
        "confusion_matrix": confusion_matrix(y_true, predictions).tolist(),
    }


def _calibration_bins(y_true: list[int], probabilities: list[float], bins: int = 5) -> list[dict[str, Any]]:
    rows = []
    for index in range(bins):
        lower = index / bins
        upper = (index + 1) / bins
        selected = [
            (label, probability)
            for label, probability in zip(y_true, probabilities)
            if lower <= probability < upper or (index == bins - 1 and probability == 1.0)
        ]
        if not selected:
            continue
        rows.append(
            {
                "bin": f"{lower:.1f}-{upper:.1f}",
                "count": len(selected),
                "mean_probability": round(sum(prob for _, prob in selected) / len(selected), 4),
                "event_rate": round(sum(label for label, _ in selected) / len(selected), 4),
            }
        )
    return rows


def run() -> dict[str, Any]:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    feature_names, x, y = _load_dataset()
    train_x, test_x, train_y, test_y = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )
    models = {
        "logistic_regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=2000, random_state=42)),
            ]
        ),
        "random_forest": RandomForestClassifier(n_estimators=120, random_state=42, min_samples_leaf=3),
    }
    model_metrics: dict[str, Any] = {}
    probabilities_by_model: dict[str, list[float]] = {}
    for name, model in models.items():
        model.fit(train_x, train_y)
        probabilities = [float(score[1]) for score in model.predict_proba(test_x)]
        probabilities_by_model[name] = probabilities
        model_metrics[name] = _metrics(test_y, probabilities)

    selected_model = max(model_metrics, key=lambda name: model_metrics[name]["roc_auc"])
    selected_probabilities = probabilities_by_model[selected_model]
    selected_metrics = model_metrics[selected_model]
    payload = {
        "dataset": "Wisconsin Diagnostic Breast Cancer public dataset",
        "rows": len(y),
        "train_rows": len(train_y),
        "test_rows": len(test_y),
        "selected_model": selected_model,
        "models": model_metrics,
        **selected_metrics,
        "boundary": "Public real-data proxy only; not a clinical, credit, legal, or production model.",
    }
    (ARTIFACT_DIR / "metrics.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    (ARTIFACT_DIR / "calibration.json").write_text(
        json.dumps({"model": selected_model, "bins": _calibration_bins(test_y, selected_probabilities)}, indent=2),
        encoding="utf-8",
    )
    with (ARTIFACT_DIR / "confusion_matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["", "predicted_0", "predicted_1"])
        matrix = selected_metrics["confusion_matrix"]
        writer.writerow(["actual_0", *matrix[0]])
        writer.writerow(["actual_1", *matrix[1]])
    importances = []
    selected = models[selected_model]
    if selected_model == "random_forest":
        importance_values = selected.feature_importances_
    else:
        importance_values = abs(selected.named_steps["model"].coef_[0])
    for feature, value in sorted(zip(feature_names, importance_values), key=lambda item: float(item[1]), reverse=True)[:12]:
        importances.append({"feature": feature, "importance": round(float(value), 6)})
    with (ARTIFACT_DIR / "feature_importance.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["feature", "importance"])
        writer.writeheader()
        writer.writerows(importances)
    (ARTIFACT_DIR / "model_card.md").write_text(
        "# Public Risk ML Model Card\n\n"
        f"Selected model: `{selected_model}`\n\n"
        f"ROC-AUC: `{selected_metrics['roc_auc']}`\n\n"
        "Intended use: portfolio evidence for baseline ML lifecycle handling.\n\n"
        "Out of scope: clinical, legal, credit, or automated decision use.\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "data_card.md").write_text(
        "# Public Risk ML Data Card\n\n"
        "Dataset: Wisconsin Diagnostic Breast Cancer public dataset via scikit-learn.\n\n"
        "Use here: real-data ML proxy for reproducible portfolio evidence.\n\n"
        "Limitations: compact tabular dataset, not representative of regulated credit/governance operations.\n",
        encoding="utf-8",
    )
    return payload


def main() -> None:
    result = run()
    print(
        "Public risk ML lab completed: "
        f"rows={result['rows']} selected_model={result['selected_model']} "
        f"roc_auc={result['roc_auc']} f1={result['f1']}"
    )


if __name__ == "__main__":
    main()
