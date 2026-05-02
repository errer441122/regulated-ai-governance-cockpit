# Credit-Risk 5-Minute Route

Use this route for a fast technical screen of the credit-risk depth. It is public-data portfolio evidence, not a CRIF system, not a bank model, and not a production approval workflow.

## Open These Files In Order

1. `credit-risk-model-risk-lab/README.md`
2. `credit-risk-model-risk-lab/reports/evaluation_metrics.json`
3. `credit-risk-model-risk-lab/reports/model_card.md`
4. `credit-risk-model-risk-lab/reports/validation_report.md`
5. `credit-risk-model-risk-lab/reports/calibration_report.md`
6. `credit-risk-model-risk-lab/reports/drift_report.html`
7. `.github/workflows/validate.yml`

## What This Shows

| Signal | Evidence |
| --- | --- |
| Public-data credit-risk modelling | OpenML GiveMeSomeCredit pipeline |
| Model comparison | `reports/training_summary.json` |
| Calibration and validation | `reports/calibration_report.md`, `reports/validation_report.md` |
| Drift monitoring | `reports/score_psi.json`, `reports/drift_report.html` |
| Threshold discussion | `reports/threshold_review.csv` |
| Explainability | `reports/feature_importance.csv` |
| Proxy/fairness awareness | `reports/validation_report.md` |
| FastAPI-style scoring boundary | `production-sim-stack/src/api.py`, `production-sim-stack/tests/test_stack.py` |
| CI evidence | `.github/workflows/validate.yml` |

## Reproduce Locally

```bash
python credit-risk-model-risk-lab/src/evaluate.py
python -m pytest -q credit-risk-model-risk-lab/tests
python -m pytest -q production-sim-stack/tests
```

## Honest Boundary

The lab uses a public competition dataset. It does not include real applicant workflow data, rejected-applicant populations, lender policies, bureau data, adverse-action logic, independent validation, or regulatory approval.
