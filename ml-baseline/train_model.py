from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from regulated_risk_ml.calibration import CalibrationReporter
from regulated_risk_ml.config import ARTIFACT_DIR, DATA_PATH, MODEL_ARTIFACT_PATH, REPORT_DIR
from regulated_risk_ml.data import RiskDatasetBuilder
from regulated_risk_ml.drift import DriftAnalyzer
from regulated_risk_ml.explainability import PermutationImportanceExplainer
from regulated_risk_ml.features import FeatureEngineer, rule_baseline
from regulated_risk_ml.metrics import ModelEvaluator
from regulated_risk_ml.models import ModelTrainer
from regulated_risk_ml.report import ModelCardWriter


def build_features(row: dict[str, Any]) -> dict[str, Any]:
    """Compatibility wrapper used by older production-sim adapter code."""
    from regulated_risk_ml.api_adapter import normalize_payload

    return FeatureEngineer().transform_record(normalize_payload(row))


def _write_json(path: Path, payload: dict[str, Any] | list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_confusion_matrix(path: Path, matrix: list[list[int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["", "predicted_0", "predicted_1"])
        writer.writerow(["actual_0", matrix[0][0], matrix[0][1]])
        writer.writerow(["actual_1", matrix[1][0], matrix[1][1]])


def _write_feature_importance(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["feature", "baseline_f1", "permuted_f1", "importance", "method"])
        writer.writeheader()
        writer.writerows(rows)


def _write_predictions(path: Path, rows: list[dict[str, Any]], probabilities: list[float], labels: list[int]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["record_id", "actual", "probability", "prediction", "sector", "region"],
        )
        writer.writeheader()
        for row, probability, label in zip(rows, probabilities, labels):
            writer.writerow(
                {
                    "record_id": row["record_id"],
                    "actual": label,
                    "probability": round(probability, 4),
                    "prediction": int(probability >= 0.5),
                    "sector": row["sector"],
                    "region": row["region"],
                }
            )


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(BASE_DIR))
    except ValueError:
        return str(path)


def train(output_dir: Path = ARTIFACT_DIR) -> dict[str, Any]:
    dataset = RiskDatasetBuilder()
    rows = dataset.load_records()
    features = FeatureEngineer()
    x = features.transform_records(rows)
    y = features.labels(rows)

    trainer = ModelTrainer()
    train_x, test_x, train_y, test_y, train_rows, test_rows = trainer.split(x, y, rows)
    models = trainer.train_models(train_x, train_y)
    evaluator = ModelEvaluator()

    model_metrics: dict[str, Any] = {}
    model_probabilities: dict[str, list[float]] = {}
    for name, model in models.items():
        probabilities = [float(score[1]) for score in model.predict_proba(test_x)]
        model_probabilities[name] = probabilities
        model_metrics[name] = evaluator.evaluate_probabilities(test_y, probabilities)

    rule_predictions = trainer.rule_predictions(test_rows)
    rule_probabilities = [0.78 if prediction else 0.22 for prediction in rule_predictions]
    model_metrics["rule_baseline"] = evaluator.evaluate_probabilities(test_y, rule_probabilities)

    selected_model = max(("logistic_regression", "random_forest"), key=lambda name: model_metrics[name]["roc_auc"])
    selected = models[selected_model]
    selected_probabilities = model_probabilities[selected_model]
    selected_metrics = model_metrics[selected_model]

    calibration = {
        "model": selected_model,
        "bins": CalibrationReporter().build_bins(test_y, selected_probabilities),
        "interpretation": "Local calibration bins for synthetic portfolio data; not production calibration.",
    }
    drift_report = DriftAnalyzer().compare(train_rows, test_rows)
    importance = PermutationImportanceExplainer(features.feature_names()).explain(selected, test_x, test_y)

    output_dir.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    metrics_payload = {
        "task": "target_default_or_escalation",
        "data_path": str(DATA_PATH.relative_to(BASE_DIR)),
        "rows": len(rows),
        "train_rows": len(train_y),
        "test_rows": len(test_y),
        "selected_model": selected_model,
        "models": model_metrics,
        "roc_auc": selected_metrics["roc_auc"],
        "pr_auc": selected_metrics["pr_auc"],
        "precision": selected_metrics["precision"],
        "recall": selected_metrics["recall"],
        "f1": selected_metrics["f1"],
        "brier_score": selected_metrics["brier_score"],
        "limits": [
            "Synthetic data only.",
            "Portfolio simulation metrics, not production validation.",
            "Advisory human-review triage only.",
        ],
    }

    _write_json(output_dir / "metrics.json", metrics_payload)
    _write_json(output_dir / "calibration.json", calibration)
    _write_json(output_dir / "drift_report.json", drift_report)
    _write_confusion_matrix(output_dir / "confusion_matrix.csv", selected_metrics["confusion_matrix"])
    _write_feature_importance(output_dir / "feature_importance.csv", importance)
    ModelCardWriter(output_dir / "model_card.md").write(
        metrics=selected_metrics,
        selected_model=selected_model,
        feature_names=features.feature_names(),
        rows=len(rows),
    )

    # Keep compact reviewer examples in reports/ for backwards compatibility with existing docs.
    _write_json(REPORT_DIR / "metrics.example.json", metrics_payload)
    _write_predictions(REPORT_DIR / "predictions_sample.csv", test_rows[:20], selected_probabilities[:20], test_y[:20])
    with (REPORT_DIR / "top_coefficients.example.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["feature", "importance", "method"])
        writer.writeheader()
        writer.writerows(
            {
                "feature": row["feature"],
                "importance": row["importance"],
                "method": row["method"],
            }
            for row in importance[:12]
        )

    try:
        import joblib

        joblib.dump(
            {
                "model": selected,
                "selected_model": "sklearn_artifact",
                "selected_algorithm": selected_model,
                "feature_names": features.feature_names(),
                "metrics": selected_metrics,
                "decision_boundary": "advisory human-review triage only",
            },
            MODEL_ARTIFACT_PATH,
        )
        artifact_status = str(MODEL_ARTIFACT_PATH.relative_to(BASE_DIR))
    except ModuleNotFoundError:
        artifact_status = "joblib unavailable; model artifact not written"

    return {
        "rows": len(rows),
        "selected_model": selected_model,
        "metrics": selected_metrics,
        "artifact": artifact_status,
        "outputs": [
            _display_path(output_dir / "metrics.json"),
            _display_path(output_dir / "calibration.json"),
            _display_path(output_dir / "drift_report.json"),
            _display_path(output_dir / "model_card.md"),
        ],
    }


def main() -> None:
    result = train()
    metrics = result["metrics"]
    print(
        "Risk ML baseline completed: "
        f"rows={result['rows']} selected_model={result['selected_model']} "
        f"roc_auc={metrics['roc_auc']} pr_auc={metrics['pr_auc']} "
        f"f1={metrics['f1']} brier={metrics['brier_score']} "
        f"artifact={result['artifact']}"
    )


if __name__ == "__main__":
    main()
