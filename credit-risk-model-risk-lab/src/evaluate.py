from __future__ import annotations

import json
from pathlib import Path

import joblib

from data import FEATURE_COLUMNS, split_dataset
from metrics import calibration_bins, classification_metrics, population_stability_index
from train import MODEL_PATH, train


BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = BASE_DIR / "reports"
METRICS_PATH = REPORT_DIR / "evaluation_metrics.json"
CALIBRATION_PATH = REPORT_DIR / "calibration_report.md"
DRIFT_PATH = REPORT_DIR / "drift_report.html"
MODEL_CARD_PATH = REPORT_DIR / "model_card.md"
FRAMEWORK_PATH = REPORT_DIR / "model_risk_framework.md"
PSI_PATH = REPORT_DIR / "score_psi.json"


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row[column]) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def write_reports(metrics: dict[str, object], bins: list[dict[str, float]], psi: dict[str, object]) -> None:
    MODEL_CARD_PATH.write_text(
        f"""# Model Card - GiveMeSomeCredit Credit-Risk Baseline

## Scope

Public-data credit-risk baseline for model-risk documentation practice. This model estimates the probability of `FinancialDistressNextTwoYears` on the OpenML curation of the original Kaggle Give Me Some Credit dataset.

## Dataset

- OpenML dataset id: `46929`
- Name: `GiveMeSomeCredit`
- Rows used: `{metrics['rows']}`
- Target event rate in test split: `{metrics['event_rate']}`
- Original source: `https://www.kaggle.com/competitions/GiveMeSomeCredit`
- OpenML metadata: `https://api.openml.org/api/v1/json/data/46929`

## Model

- Selected model: `{metrics['selected_model']}`
- Split: stratified 80/20, random state 42
- Features: `{', '.join(FEATURE_COLUMNS)}`

## Metrics

- ROC-AUC: `{metrics['roc_auc']}`
- PR-AUC: `{metrics['pr_auc']}`
- Gini: `{metrics['gini']}`
- KS statistic: `{metrics['ks_statistic']}`
- Brier score: `{metrics['brier_score']}`
- Expected calibration error: `{metrics['expected_calibration_error']}`
- Score PSI train vs test: `{psi['psi']}`

## Intended Use

Portfolio evidence for credit-risk ML, calibration, drift monitoring, and model-risk documentation.

## Not For

- production lending decisions
- automated credit approval or denial
- legal or regulatory compliance certification
- CRIF, bank, or client deployment claims

## Human Review Boundary

Any score is advisory evidence only. No individual decision should be made from this model.
""",
        encoding="utf-8",
    )

    CALIBRATION_PATH.write_text(
        "# Calibration Report\n\n"
        f"Expected calibration error: `{metrics['expected_calibration_error']}`\n\n"
        + markdown_table(bins, ["bin", "low", "high", "count", "mean_score", "event_rate"])
        + "\n",
        encoding="utf-8",
    )

    DRIFT_PATH.write_text(
        """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Credit Risk Drift Report</title></head>
<body>
<h1>Credit Risk Drift Report</h1>
<p>Population stability index compares train-score distribution against test-score distribution.</p>
"""
        + f"<p><strong>Score PSI:</strong> {psi['psi']}</p>\n"
        + "<table><thead><tr><th>Bin</th><th>Expected %</th><th>Actual %</th><th>Contribution</th></tr></thead><tbody>\n"
        + "\n".join(
            f"<tr><td>{row['bin']}</td><td>{row['expected_pct']}</td><td>{row['actual_pct']}</td><td>{row['contribution']}</td></tr>"
            for row in psi["bins"]
        )
        + "\n</tbody></table>\n"
        + "<p>Boundary: public-data portfolio evidence only, not production monitoring.</p>\n"
        + "</body></html>\n",
        encoding="utf-8",
    )

    FRAMEWORK_PATH.write_text(
        """# Model Risk Framework - Public Credit-Risk Baseline

## Governance

The model is owned as a portfolio artifact. Its scope, data source, intended use, limitations, and change history must remain visible in the repository.

## Validation Checklist

| Control | Evidence |
| --- | --- |
| Public data source recorded | `README.md`, `data/openml_46929_metadata.json` when fetched |
| Train/test split defined | `reports/training_summary.json` |
| Domain metrics reported | `reports/evaluation_metrics.json` |
| Calibration assessed | `reports/calibration_report.md` |
| Drift/PSI assessed | `reports/drift_report.html`, `reports/score_psi.json` |
| Human-review boundary stated | `reports/model_card.md` |

## Model Change Policy

Any future model change should record dataset version, feature changes, training parameters, metric movement, and known limitations before being described publicly.

## Residual Risks

- competition dataset may not reflect current lending populations
- no protected-class fairness analysis
- no production monitoring or challenger governance
- no regulatory approval or independent validation
""",
        encoding="utf-8",
    )


def evaluate() -> dict[str, object]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    if not MODEL_PATH.exists():
        train()
    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    x_train, x_test, y_train, y_test = split_dataset()
    train_score = model.predict_proba(x_train)[:, 1]
    test_score = model.predict_proba(x_test)[:, 1]
    metrics = classification_metrics(y_test, test_score)
    metrics.update(
        {
            "selected_model": bundle["selected_model"],
            "dataset": bundle["dataset"],
            "feature_columns": bundle["feature_columns"],
        }
    )
    bins = calibration_bins(y_test, test_score)
    psi = population_stability_index(train_score, test_score)

    METRICS_PATH.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    PSI_PATH.write_text(json.dumps(psi, indent=2, sort_keys=True), encoding="utf-8")
    write_reports(metrics, bins, psi)
    return metrics


def main() -> None:
    print(json.dumps(evaluate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
