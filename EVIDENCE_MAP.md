# Evidence Map - AI, Data, Governance, and Innovation Roles

This file maps target-role requirements to concrete repository evidence. It favors inspectable files, commands, tests, and generated artifacts over broad claims.

## Main Project Evidence

| Target role / employer type | Requirement signal | Where the reviewer can inspect it | Evidence shown | Honest gap |
| --- | --- | --- | --- | --- |
| CRIF ML Engineering | Python/OOP, ML, data quality, web-framework interest, data-engineering decomposition | `credit-risk-model-risk-lab/`, `ml-baseline/`, `orchestration/`, `production-sim-stack/src/ml_model_adapter.py`, `sql/`, `hpc/` | Public GiveMeSomeCredit risk model, Gini/KS/Brier/ECE/PSI, OOP-style risk ML pipeline, drift/data-quality report, FastAPI-compatible adapter, SQL mart, Slurm packaging | No real CRIF data, no production cloud or SaaS integration |
| CRIF Data Enhancement | verification, correctness checks, updating/anomaly mindset | `ml-baseline/artifacts/drift_report.json`, `scripts/validate-data.mjs`, `technical-lab/`, `ai-data-agentic-readiness-lab/` | Schema checks, missing-rate report, readiness validation, deterministic audit logs | Synthetic records, no real company registry workflow |
| PwC Data & AI Consulting | data-to-insight storytelling, SQL, dashboard, ML, stakeholder communication | cockpit UI, `README.md`, `docs/reviewer/`, `sql/`, `production-sim-stack/` | Consulting-style narrative, dashboard logic, SQL marts, local API scoring simulation, model card, calibration outputs | No client deployment or production platform |
| PwC Risk ML | classification, calibration, model comparison, backtesting-style metrics | `credit-risk-model-risk-lab/reports/evaluation_metrics.json`, `credit-risk-model-risk-lab/reports/calibration_report.md`, `credit-risk-model-risk-lab/reports/drift_report.html`, `ml-baseline/train_model.py` | Public-data ROC-AUC, PR-AUC, Gini, KS, Brier score, ECE, PSI, calibration bins, model card, model-risk framework | Public competition data, no client delivery or production validation |
| UNDP Digital/Data Science | public data, SDG framing, responsible data, NLP/text mining, policy note | `undp-sdg-risk-lab/`, `production-sim-stack/PUBLIC_SECTOR_SDG_ROUTE.md`, `UNDP_REVIEWER_ROUTE.md` | Offline public-development-style dataset, TF-IDF/topic keywords, responsible checklist, SDG policy note, public-sector triage boundary | Not a real UNDP project, no country-office validation |
| CINECA / IT4LIA | Slurm, Linux batch, AI workload, benchmark, metadata, container packaging, trust/compliance | `hpc/`, `hpc-ai-rag-lab/`, `ai-factory-workload-pack/`, `CINECA_IT4LIA_REVIEWER_ROUTE.md` | Slurm scripts, Apptainer recipe, retrieval benchmark, workload manifest, FAIR metadata, data management plan | No real cluster, GPU, Leonardo, or AI Factory execution |
| BI-REX supplement | data engineering, monitoring, Slurm, industrial AI awareness | `production-sim-stack/`, `hpc-mlops-industrial-lab/`, `hpc/` | Influx/Grafana-style artifacts, batch scoring, industrial-style failure signals, Slurm packaging | Ducati repo remains stronger for industrial telemetry |

## Reviewer Shortcut For Technical Gaps

| If the reviewer is checking for... | Inspect this first | Evidence now present |
| --- | --- | --- |
| Real public credit-risk data | `credit-risk-model-risk-lab/README_RECRUITER.md`, `credit-risk-model-risk-lab/reports/evaluation_metrics.json`, `credit-risk-model-risk-lab/src/train.py` | OpenML GiveMeSomeCredit, 150k rows, Gini, KS, Brier, ECE, PSI, model card |
| ML baseline and model evaluation | `ml-baseline/src/regulated_risk_ml/`, `ml-baseline/train_model.py`, `ml-baseline/artifacts/metrics.json` | train/test split, Logistic Regression, RandomForest comparison, ROC-AUC, PR-AUC, Brier score, confusion matrix, calibration bins |
| OOP / pipeline engineering | `ml-baseline/src/regulated_risk_ml/`, `orchestration/local_orchestrator.py`, `production-sim-stack/src/pipeline.py` | classes for data, features, training, metrics, drift, model card, plus local orchestration decomposition |
| Explainability and model limits | `ml-baseline/artifacts/feature_importance.csv`, `ml-baseline/artifacts/model_card.md` | permutation-style importance or fallback importance and explicit human-review boundary |
| Data quality and drift | `ml-baseline/artifacts/drift_report.json`, `technical-lab/src/validate_dataset.py` | schema validation, missing-rate checks, PSI-like drift summary |
| Governance framework mapping | `governance/nist_ai_rmf_mapping.csv`, `governance/eu_ai_act_gap_analysis.md`, `governance/iso42001_public_gap_analysis.md` | NIST AI RMF function mapping, EU AI Act gap analysis, public ISO/IEC 42001 gap analysis |
| SQL / analytics engineering | `sql/reviewer_feature_mart.duckdb.sql`, `production-sim-stack/sql/feature_mart.duckdb.sql`, `hpc-mlops-industrial-lab/sql/build_feature_mart.sql` | DuckDB/SQLite feature mart designs and reviewer shortcuts |
| Cloud / lifecycle simulation | `https://regulated-ai-governance-api.onrender.com/docs`, `README_DEPLOYMENT.md`, `render.yaml`, `production-sim-stack/Dockerfile`, `production-sim-stack/docker-compose.yml`, `production-sim-stack/docs/architecture.md`, `evidence/docker-smoke-test.md`, `evidence/deployment_evidence.md` | Live Render API proof-of-execution, FastAPI-compatible API, Docker Compose, MLflow-like metadata, MinIO-like manifest, smoke-test record, live-deploy evidence |
| HPC / Slurm evidence | `hpc/`, `hpc-ai-rag-lab/slurm/run_rag_benchmark.sbatch`, `production-sim-stack/slurm/run_capacity_scoring_array.sbatch`, `ai-factory-workload-pack/` | batch scripts, job array script, local benchmark, workload manifest, Apptainer packaging |
| UNDP public-sector framing | `undp-sdg-risk-lab/`, `production-sim-stack/data/public_development_sample.csv`, `production-sim-stack/src/fetch_world_bank_sample.py` | public-development-style sample, offline-first pipeline, policy note, responsible data checklist |

## Project Artifacts

| Artifact | Reviewer value | File / section |
| --- | --- | --- |
| Interactive cockpit | Shows dashboard, scoring, workflow, adoption, training, and product thinking in one reviewable artifact | `index.html`, `app.js`, `data.js` |
| Data validator | Shows basic quality discipline and executable validation | `scripts/validate-data.mjs` |
| Risk ML Lab | Conventional CRIF/PwC ML evidence with OOP code, model comparison, metrics, calibration, drift, and model card | `ml-baseline/` |
| Credit Risk Model Risk Lab | Public-data GiveMeSomeCredit model-risk evidence with Gini, KS, Brier, ECE, PSI, model card, calibration report, and drift report | `credit-risk-model-risk-lab/` |
| Governance Audit Pack | Structured NIST AI RMF, EU AI Act, ISO/IEC 42001 public gap mapping plus validation checklist and change log | `governance/` |
| Local orchestration path | Shows Dagster-equivalent decomposition without claiming real orchestration deployment | `orchestration/` |
| UNDP SDG risk lab | Adds public-data, NLP/topic keywords, responsible data, and policy-note evidence | `undp-sdg-risk-lab/` |
| HPC/RAG lab | Adds CPU-friendly retrieval workload, Slurm packaging, Apptainer recipe, and benchmark artifact | `hpc-ai-rag-lab/` |
| HPC/MLOps/industrial lab | Adds executable ML, text mining, GIS-lite feature engineering, SQL feature mart, model card, metrics, Slurm batch script, and orchestration adapter sketches | `hpc-mlops-industrial-lab/` |
| Production simulation stack | Adds API scoring, live Render API, deploy-ready Docker service, Render Blueprint, Docker Compose, lifecycle metadata, object-storage-style manifest, DuckDB SQL, monitoring outputs, Slurm job array, and architecture/smoke docs | `production-sim-stack/`, `render.yaml`, `README_DEPLOYMENT.md`, `evidence/deployment_evidence.md` |
| AI Factory workload pack | Makes workload packaging, metadata, data management, benchmark, and container assumptions explicit | `ai-factory-workload-pack/` |
| Technical result images | Gives fast reviewers visual proof of prior metric/model/API evidence | `evidence/technical-screenshots/` |
| Reviewer route docs | Gives recruiter and technical reviewers a low-friction route through the project | `docs/reviewer/` |

## Interview Framing

Use this project as an applied AI/data implementation case study:

> I built a regulated AI governance cockpit and hardened it with executable evidence: a public GiveMeSomeCredit credit-risk model-risk lab, a scikit-learn synthetic risk ML lab, SQL marts, FastAPI-compatible scoring, offline public-data/SDG analysis, Slurm-ready workload packaging, governance framework mapping, and reviewer route documentation. The project is deliberately honest about public data, simulated data, local-only execution, and human-review boundaries.

## What Not To Claim

- Do not claim this is a production CRM, legal compliance tool, deployed AI product, credit model, aid allocation tool, or employer system.
- Do not claim access to confidential customer, pipeline, company, public-sector, CINECA, IT4LIA, CRIF, PwC, UNDP, BI-REX, or Ducati data.
- Do not claim production MLOps, production cloud deployment, real Slurm cluster execution, or real AI Factory access. The Render URL is portfolio proof-of-execution only.
- Do claim workflow design, analytics reasoning, documentation discipline, responsible AI framing, and junior-level technical implementation.
