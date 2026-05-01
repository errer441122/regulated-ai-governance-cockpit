# Model Change Log

| Date | Artifact | Change | Evidence | Risk Note |
| --- | --- | --- | --- | --- |
| 2026-05-01 | production-sim-stack API | Added deploy-ready API contract with `/metadata`, `/score`, OpenAPI docs, Dockerfile, and Render Blueprint | `README_DEPLOYMENT.md`, `render.yaml`, `production-sim-stack/tests/test_stack.py` | Deploy-ready only until live URL is recorded |
| 2026-05-01 | credit-risk-model-risk-lab | Added public-data GiveMeSomeCredit baseline with Gini, KS, Brier, ECE, PSI, calibration, drift, and model card outputs | `credit-risk-model-risk-lab/reports/` | Public competition data; not a production credit model |
| 2026-05-01 | governance audit pack | Added NIST AI RMF, EU AI Act, and ISO/IEC 42001 public mapping docs | `governance/` | Public-source gap analysis only |

## Required Fields For Future Changes

Every future model or API change should record:

- dataset version or source change
- feature or target definition change
- model family and parameter change
- metric movement against prior version
- calibration and drift impact
- known limitation or residual risk
- reviewer/approver, if used outside portfolio review
