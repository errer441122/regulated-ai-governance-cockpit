# Portfolio Evidence Report

Generated at: 2026-05-01T17:25:54+00:00

## Executive Summary

This Evidence Lock turns the repository from a static dashboard-first portfolio into a Python/ML-first evidence package. The static cockpit remains a demo layer; the permanent reviewer signal is executable Python, scikit-learn models, data-quality checks, drift/calibration artifacts, public-data lab outputs, API smoke evidence, Docker evidence, and Slurm/HPC portability files.

## Reproducibility

```bash
make setup
make evidence
```

Equivalent shell steps are listed in `evidence-lock/commands.sh`.

## Main ML Baseline

| Evidence | Value |
| --- | --- |
| Dataset | ml-baseline/data/simulated_regulated_risk_dataset.csv |
| Rows | 360 |
| Model | Logistic Regression + RandomForest baseline |
| Selected model | logistic_regression |
| ROC-AUC | 0.996 |
| PR-AUC | 0.976 |
| F1 | 0.8667 |
| Recall | 1.0 |
| Brier score | 0.0301 |
| Calibration | included |
| Drift check | included |
| Data quality | passed |

## Public Real-Data Lab

| Evidence | Value |
| --- | --- |
| Dataset | Wisconsin Diagnostic Breast Cancer public dataset |
| Source | UCI / scikit-learn Wisconsin Diagnostic Breast Cancer dataset |
| Selected model | logistic_regression |
| ROC-AUC | 0.9962 |
| F1 | 0.9515 |
| Brier score | 0.0224 |

## API, Docker, and Operations Evidence

| Check | Status |
| --- | --- |
| API smoke test | `evidence-lock/results/api_smoke_test.md` |
| Docker smoke test | `evidence-lock/results/docker_smoke_test.md` |
| Model card | `evidence-lock/results/model_card.md` |
| Data card | `evidence-lock/results/data_card.md` |
| Limitations | `evidence-lock/results/limitations.md` |
| Screenshots | `evidence-lock/results/screenshots/` |
| Terminal logs | `evidence-lock/results/terminal_logs/` |

## UNDP Public Data / GIS-Lite Evidence

| Evidence | Value |
| --- | --- |
| Rows | 4 |
| Average SDG risk score | 0.5039 |
| Map output | `undp-public-data-gis-lab/artifacts/map_output.png` |
| Policy note | `undp-public-data-gis-lab/artifacts/policy_note.md` |

## CINECA / IT4LIA AI/HPC Evidence

| Evidence | Value |
| --- | --- |
| Benchmark backend | numpy_fallback_no_torch |
| Runtime seconds | 0.0002 |
| Inference latency ms | 0.0053 |
| Execution note | Executed locally on CPU with NumPy fallback because PyTorch is optional in CI. |

## Scope Boundaries

This is not a production system, not a legal compliance tool, not a credit model, not an aid-allocation tool, and not a real CINECA/IT4LIA/CRIF/PwC/UNDP/BI-REX deployment.
