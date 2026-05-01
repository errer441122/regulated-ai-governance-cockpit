# Risk ML Lab - Scikit-learn Baseline

This folder is the reviewer-visible CRIF/PwC Risk ML Lab for the regulated AI governance cockpit.

It uses synthetic regulated-risk records only. The task is advisory: estimate whether a simulated regulated workflow should be escalated to human review or default/escalation monitoring. It must not be used as a production credit, eligibility, procurement, aid allocation, legal, or customer decision system.

## What It Shows

- OOP-style Python components under `src/regulated_risk_ml/`.
- Deterministic synthetic dataset generation with at least 300 rows.
- Train/test split with fixed random seed.
- Logistic Regression baseline.
- RandomForest comparison.
- Transparent rule baseline for fallback.
- ROC-AUC, PR-AUC, F1, precision, recall, confusion matrix, and Brier score.
- Calibration bins in `artifacts/calibration.json`.
- Data quality and PSI-like drift report in `artifacts/drift_report.json`.
- Permutation-style feature importance in `artifacts/feature_importance.csv`.
- Generated model card in `artifacts/model_card.md`.
- Optional `model.joblib` artifact when joblib is available.
- API scoring bridge through `production-sim-stack/src/ml_model_adapter.py`.

## Run

```bash
python -m pip install -r ml-baseline/requirements.txt
python ml-baseline/train_model.py
python -m pytest -q ml-baseline/tests
```

Expected generated artifacts:

- `artifacts/metrics.json`
- `artifacts/calibration.json`
- `artifacts/confusion_matrix.csv`
- `artifacts/feature_importance.csv`
- `artifacts/drift_report.json`
- `artifacts/model_card.md`
- `artifacts/model.joblib` if joblib is available

## Boundary

This is a compact portfolio ML baseline, not a production ML lifecycle. The dataset is generated locally from deterministic synthetic rules. Metrics are useful for code review and interview discussion only.
