# Recruiter Route - Credit Risk Model Risk Lab

Review this folder when checking whether the portfolio goes beyond simulated commercial data.

Fast path:

1. `reports/evaluation_metrics.json` for ROC-AUC, PR-AUC, Gini, KS, Brier, ECE, and PSI.
2. `reports/model_card.md` for intended use, limits, dataset source, and human-review boundary.
3. `reports/calibration_report.md` for probability calibration checks.
4. `reports/drift_report.html` for population stability evidence.
5. `src/train.py` and `src/evaluate.py` for reproducible execution.

Positioning:

> Public competition credit-risk baseline with model-risk documentation, calibration, drift checks, and financial-risk metrics. Not a production credit model.

Why this matters:

- uses a real public credit-risk dataset, not synthetic CRM labels
- includes domain metrics beyond generic accuracy
- keeps model-risk claims explicit and bounded
- separates execution evidence from legal/compliance claims
