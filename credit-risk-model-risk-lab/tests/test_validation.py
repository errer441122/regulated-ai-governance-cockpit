from pathlib import Path
import sys

import numpy as np
from sklearn.linear_model import LogisticRegression


BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from validation import (  # noqa: E402
    monitoring_plan,
    permutation_importance_rows,
    proxy_variable_notes,
    render_validation_report,
)
import evaluate as evaluate_module  # noqa: E402


def test_proxy_variable_notes_call_out_credit_risk_proxy_features():
    notes = proxy_variable_notes(["age", "MonthlyIncome", "DebtRatio", "NumberOfDependents"])

    reviewed_features = {row["feature"] for row in notes}
    assert {"age", "MonthlyIncome", "DebtRatio", "NumberOfDependents"} <= reviewed_features
    assert any("protected-class proxy" in row["review_note"] for row in notes)
    assert all(row["action"] for row in notes)


def test_permutation_importance_rows_are_sorted_and_named():
    x_train = np.array(
        [
            [0.0, 0.0],
            [0.1, 0.0],
            [0.8, 0.1],
            [0.9, 0.2],
            [0.2, 0.9],
            [0.7, 0.8],
        ]
    )
    y_train = np.array([0, 0, 1, 1, 0, 1])
    model = LogisticRegression().fit(x_train, y_train)

    rows = permutation_importance_rows(
        model,
        x_train,
        y_train,
        ["utilization", "income_missing"],
        n_repeats=2,
        random_state=7,
    )

    assert [row["rank"] for row in rows] == [1, 2]
    assert {row["feature"] for row in rows} == {"utilization", "income_missing"}
    assert rows[0]["importance_mean"] >= rows[1]["importance_mean"]


def test_validation_report_contains_model_risk_screening_sections():
    report = render_validation_report(
        metrics={"roc_auc": 0.81, "pr_auc": 0.42, "brier_score": 0.05, "expected_calibration_error": 0.02},
        psi={"psi": 0.018},
        thresholds=[
            {"threshold": 0.1, "review_rate": 0.35, "precision": 0.24, "recall": 0.72},
            {"threshold": 0.5, "review_rate": 0.04, "precision": 0.61, "recall": 0.21},
        ],
        feature_importance=[
            {"rank": 1, "feature": "RevolvingUtilizationOfUnsecuredLines", "importance_mean": 0.12, "importance_std": 0.01}
        ],
        proxy_notes=proxy_variable_notes(["age", "MonthlyIncome"]),
        production_monitoring=monitoring_plan(),
        training_summary={
            "selected_model": "hist_gradient_boosting_probability",
            "candidate_metrics": {
                "logistic_regression_balanced": {"roc_auc": 0.78, "brier_score": 0.06},
                "hist_gradient_boosting_probability": {"roc_auc": 0.81, "brier_score": 0.05},
            },
        },
    )

    assert "# Credit-Risk Validation Report" in report
    assert "Model Comparison" in report
    assert "Calibration And Drift" in report
    assert "Reject-Inference Boundary" in report
    assert "Proxy / Fairness Review" in report
    assert "Production Monitoring Plan" in report


def test_write_reports_materializes_validation_and_importance_artifacts(tmp_path, monkeypatch):
    monkeypatch.setattr(evaluate_module, "MODEL_CARD_PATH", tmp_path / "model_card.md")
    monkeypatch.setattr(evaluate_module, "CALIBRATION_PATH", tmp_path / "calibration_report.md")
    monkeypatch.setattr(evaluate_module, "DRIFT_PATH", tmp_path / "drift_report.html")
    monkeypatch.setattr(evaluate_module, "FRAMEWORK_PATH", tmp_path / "model_risk_framework.md")
    monkeypatch.setattr(evaluate_module, "THRESHOLD_PATH", tmp_path / "threshold_review.csv")
    monkeypatch.setattr(evaluate_module, "VALIDATION_PATH", tmp_path / "validation_report.md")
    monkeypatch.setattr(evaluate_module, "FEATURE_IMPORTANCE_PATH", tmp_path / "feature_importance.csv")

    metrics = {
        "dataset_rows": 100,
        "train_rows": 80,
        "test_rows": 20,
        "event_rate": 0.1,
        "selected_model": "hist_gradient_boosting_probability",
        "roc_auc": 0.81,
        "pr_auc": 0.42,
        "gini": 0.62,
        "ks_statistic": 0.41,
        "brier_score": 0.05,
        "expected_calibration_error": 0.02,
    }
    bins = [{"bin": 1, "low": 0.0, "high": 0.1, "count": 4, "mean_score": 0.04, "event_rate": 0.05}]
    psi = {"psi": 0.018, "bins": [{"bin": 1, "expected_pct": 0.5, "actual_pct": 0.5, "contribution": 0.0}]}
    thresholds = [{"threshold": 0.1, "review_rate": 0.35, "precision": 0.24, "recall": 0.72, "false_positive_rate": 0.2, "true_positive": 3, "false_positive": 7, "false_negative": 1, "true_negative": 9}]
    feature_importance = [{"rank": 1, "feature": "age", "importance_mean": 0.04, "importance_std": 0.01}]
    training_summary = {
        "selected_model": "hist_gradient_boosting_probability",
        "candidate_metrics": {"hist_gradient_boosting_probability": {"roc_auc": 0.81, "pr_auc": 0.42, "brier_score": 0.05}},
    }

    evaluate_module.write_reports(metrics, bins, psi, thresholds, feature_importance, training_summary)

    assert (tmp_path / "validation_report.md").exists()
    assert (tmp_path / "feature_importance.csv").exists()
    assert "Reject-Inference Boundary" in (tmp_path / "validation_report.md").read_text(encoding="utf-8")
