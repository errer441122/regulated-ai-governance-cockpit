# Model Card - Regulated Risk ML Lab

This static card describes the lab design. The current run-specific model card is generated at `ml-baseline/artifacts/model_card.md` by `python ml-baseline/train_model.py`.

## Model Summary

The lab trains Logistic Regression and RandomForest baselines on a deterministic synthetic regulated-risk dataset. It selects the stronger local model by ROC-AUC and writes metrics, calibration, drift, feature importance, and model-card artifacts.

## Intended Use

- Reviewer-visible ML engineering evidence for CRIF/PwC-style screening.
- Advisory human-review triage for simulated regulated workflows.
- Discussion of calibration, drift, model comparison, and transparent fallback logic.

## Not Intended For

- Credit, eligibility, procurement, legal, public-service, aid allocation, or customer decisions.
- Automated enforcement or operational routing.
- Claims of production MLOps, fairness certification, real cloud deployment, or real Slurm execution.

## Inputs

The generated dataset contains synthetic fields such as company age, sector risk, data quality, financial signal, ESG/climate exposure, late-payment signal, region macro risk, text risk, and geographic distance risk.

## Outputs

- `ml-baseline/artifacts/metrics.json`
- `ml-baseline/artifacts/calibration.json`
- `ml-baseline/artifacts/confusion_matrix.csv`
- `ml-baseline/artifacts/feature_importance.csv`
- `ml-baseline/artifacts/drift_report.json`
- `ml-baseline/artifacts/model_card.md`
- `ml-baseline/artifacts/model.joblib` when joblib is available

## Limitations

- Synthetic dataset and labels.
- No fairness certification or legal review.
- No production monitoring, retraining automation, or model registry.
- Human-review boundary is mandatory.
