# Model Risk Framework - Public Credit-Risk Baseline

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
| Threshold sensitivity reviewed | `reports/threshold_review.csv` |
| Explainability reviewed | `reports/feature_importance.csv` |
| Validation narrative | `reports/validation_report.md` |
| Human-review boundary stated | `reports/model_card.md` |

## Model Change Policy

Any future model change should record dataset version, feature changes, training parameters, metric movement, and known limitations before being described publicly.

## Residual Risks

- competition dataset may not reflect current lending populations
- no protected-class fairness analysis
- no production monitoring or challenger governance
- no regulatory approval or independent validation
