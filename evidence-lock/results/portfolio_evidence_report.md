# Portfolio Evidence Report

Generated at: 2026-05-02T11:49:50+00:00

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

## Public Credit-Risk Model-Risk Lab

| Evidence | Value |
| --- | --- |
| Dataset | OpenML 46929 GiveMeSomeCredit |
| Dataset rows | 150000 |
| Evaluation rows | 30000 |
| Selected model | hist_gradient_boosting_probability |
| ROC-AUC | 0.870866 |
| Gini | 0.741732 |
| KS statistic | 0.593015 |
| Brier score | 0.04843 |
| Expected calibration error | 0.003949 |
| Model card | `credit-risk-model-risk-lab/reports/model_card.md` |
| Validation report | `credit-risk-model-risk-lab/reports/validation_report.md` |
| Feature importance | `credit-risk-model-risk-lab/reports/feature_importance.csv` |
| Threshold review | `credit-risk-model-risk-lab/reports/threshold_review.csv` |

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

## UNDP AI for SDGs Policy Evidence

| Evidence | Value |
| --- | --- |
| Rows | 10 |
| Capacity-support flags | 3 |
| Average SDG risk score | 0.3748 |
| Top contexts | HTI, NPL, BGD |
| Policy brief | `undp-sdg-risk-lab/artifacts/ai_for_sdgs_policy_brief.md` |
| Charts | `undp-sdg-risk-lab/artifacts/ai_for_sdgs_risk_ranking.svg`, `undp-sdg-risk-lab/artifacts/ai_for_sdgs_indicator_heatmap.svg` |

## CINECA / IT4LIA AI/HPC Evidence

| Evidence | Value |
| --- | --- |
| Benchmark backend | numpy_fallback_no_torch |
| Runtime seconds | 0.0002 |
| Inference latency ms | 0.0053 |
| Execution note | Executed locally on CPU with NumPy fallback because PyTorch is optional in CI. |

## Governance / SDG RAG Evidence

| Evidence | Value |
| --- | --- |
| Documents | 7 |
| Chunks | 15 |
| Eval questions | 10 |
| Answerable questions | 7 |
| Adversarial questions | 3 |
| Top-k accuracy | 0.7 |
| Grounding coverage | 0.7 |
| Documented failures | 3 |
| Mean hallucination risk score | 0.272 |
| Source manifest | `hpc-ai-rag-lab/data/source_manifest.json` |
| FastAPI-compatible endpoint | `hpc-ai-rag-lab/src/api.py` |

## Industrial AI Supplement Evidence

| Evidence | Value |
| --- | --- |
| Telemetry schema | mqtt-opcua-telemetry |
| Anomaly threshold | 0.5 |
| Alert rate | 0.125 |
| Alerts | 3 |
| Public dataset manifest | `hpc-mlops-industrial-lab/data/public_industrial_dataset_manifest.json` |
| Demo payload | `hpc-mlops-industrial-lab/demo/telemetry_payload.json` |
| Curl demo script | `docs/reviewer/BI_REX_DEMO_SCRIPT.md` |
| Reviewer route | `docs/reviewer/BI_REX_INDUSTRIAL_AI_ROUTE.md` |

## Scope Boundaries

This is not a production system, not a legal compliance tool, not a credit model, not an aid-allocation tool, and not a real CINECA/IT4LIA/CRIF/PwC/UNDP/BI-REX deployment.
