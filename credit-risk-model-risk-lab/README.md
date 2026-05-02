# Credit Risk Model Risk Lab

This lab is a real public-data credit-risk baseline for CRIF/PwC-style review.

It uses the OpenML public curation of the original Kaggle Give Me Some Credit competition dataset:

- OpenML dataset id: `46929`
- dataset name: `GiveMeSomeCredit`
- rows: `150000`
- target: `FinancialDistressNextTwoYears`
- original source: `https://www.kaggle.com/competitions/GiveMeSomeCredit`
- OpenML metadata: `https://api.openml.org/api/v1/json/data/46929`

This is not a production credit model and is not suitable for lending decisions. It is a portfolio model-risk exercise on a public competition dataset.

## Run

```bash
python -m pip install -r credit-risk-model-risk-lab/requirements.txt
python credit-risk-model-risk-lab/src/fetch_data.py
python credit-risk-model-risk-lab/src/train.py
python credit-risk-model-risk-lab/src/evaluate.py
```

Generated evidence:

- `reports/evaluation_metrics.json`
- `reports/model_card.md`
- `reports/validation_report.md`
- `reports/calibration_report.md`
- `reports/drift_report.html`
- `reports/feature_importance.csv`
- `reports/model_risk_framework.md`
- `reports/score_psi.json`
- `reports/threshold_review.csv`
- `reports/training_summary.json`

## Metrics

The evaluation reports ROC-AUC, PR-AUC, Gini, KS statistic, Brier score, expected calibration error, confusion matrix counts, population stability index, threshold operating points, permutation importance, proxy/fairness notes, reject-inference boundaries, and a production monitoring checklist for reviewer discussion.

Fast route: `docs/reviewer/CRIF_5_MIN_ROUTE.md`.

## Boundary

Use this as evidence of public-data risk modeling, calibration thinking, drift monitoring, and model-risk documentation. Do not claim it is a CRIF model, a lending system, a regulatory-compliant model, or a production MRM framework.
