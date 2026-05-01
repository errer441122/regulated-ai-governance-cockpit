# Pull Request Description

## Objective

This PR hardens the repository as an AI/Data internship portfolio project. It makes the project easier for recruiters to scan, more credible for technical reviewers to verify, and more explicit about what is simulated versus actually executable.

## What Changed

### Recruiter-facing documentation

- Added reviewer routes, fit summaries, evidence maps, and limitation notes.
- Clarified the repository positioning for AI/Data, governance, risk, public-sector, and HPC-oriented internships.

### Technical reviewer route

- Added a 20-minute technical review path covering ML training, orchestration, production simulation, SDG/public-data work, and HPC/RAG evidence.
- Added a generated reviewer summary and local smoke-check script.

### ML/data pipeline evidence

- Expanded `ml-baseline/` into a reviewer-visible risk ML lab with feature engineering, model comparison, metrics, calibration, drift, feature importance, and model-card artifacts.
- Added pytest coverage for ML baseline data, features, metrics, and training behavior.

### MLOps/production-like simulation evidence

- Strengthened the local production simulation with architecture docs, API contract checks, smoke-test planning, and an adapter that can load the local ML artifact while preserving a transparent fallback.

### HPC/Slurm/AI Factory or industrial evidence

- Added and expanded Slurm-ready and AI Factory-style evidence through `hpc-ai-rag-lab/`, `ai-factory-workload-pack/`, and related reviewer docs.
- Added a local CPU-friendly retrieval/RAG benchmark, Apptainer recipe, workload manifest, and benchmark artifacts.

### Tests and reproducibility

- Added and updated `package.json`, `Makefile`, `pytest.ini`, CI workflow validation, smoke checks, and reviewer-visible artifact generation paths.
- Added local orchestration and reproducibility scripts for reviewer verification.

### Claims and limitations

- Added explicit claims boundaries covering synthetic data, local-only execution, simulated production infrastructure, and no real employer/client/HPC execution.

## Target Fit

- **CRIF:** maps to ML engineering, data quality, risk scoring, OOP-style Python, model evaluation, orchestration, SQL, and FastAPI-compatible scoring evidence.
- **PwC:** maps to Data & AI / Risk consulting through model cards, calibration/drift artifacts, SQL marts, dashboard narrative, governance framing, and technical-review documentation.
- **UNDP:** relevant through the `undp-sdg-risk-lab/` public-development-style data path, responsible data checklist, text-mining summary, and SDG policy-note artifact.
- **CINECA / IT4LIA:** maps to HPC/AI Factory readiness through Slurm packaging, Apptainer recipe, local RAG benchmark, workload manifest, metadata, and explicit no-real-cluster boundary.

## What This PR Does NOT Claim

- No real company data.
- No production deployment.
- No real cloud, HPC, Slurm, Leonardo, CINECA, IT4LIA, or AI Factory execution; current evidence is local execution plus packaging/simulation artifacts only.
- No real industrial integration.
- No employer evaluation, endorsement, client delivery, or institutional validation.

## Tests Run

- `npm test`
  - Passed. Static dataset validation passed: 20 accounts, 16 deals, 3 decision demos.
  - Python unittest suites passed: 2 HPC tests and 5 production-sim tests.

- `python -m pytest -q`
  - Passed: 22 tests passed in 1.87s.

- `python hpc-mlops-industrial-lab/src/run_pipeline.py`
  - Passed: rows=24, accuracy=0.8333, f1=0.8889.

- `python production-sim-stack/src/orchestrate.py`
  - Passed: rows=20, accuracy=0.95, f1=0.9524.

- `python ml-baseline/train_model.py`
  - Passed: rows=360, selected_model=logistic_regression, roc_auc=0.996, pr_auc=0.976, f1=0.8667, brier=0.0301.

- `python orchestration/local_orchestrator.py`
  - Passed: completed 5 steps and wrote `orchestration/run_manifest.json`.

- `python undp-sdg-risk-lab/src/run_pipeline.py`
  - Passed: rows=10, flags=3, average_score=0.3748.

- `python hpc-ai-rag-lab/src/benchmark.py --quick`
  - Passed: documents=3, chunks=6, queries=2, top_k_accuracy=1.0.

- `python production-sim-stack/scripts/check_api_contract.py`
  - Passed: returned valid regulated workflow and capacity-support contract output.

- `python scripts/smoke_check.py`
  - Passed: all required local artifacts present; missing=[].

- `python scripts/build_reviewer_summary.py`
  - Passed: wrote `docs/reviewer/REVIEWER_SUMMARY.md`.

## Remaining Gaps

- Add real Docker Compose smoke evidence only after rerunning and documenting the local container flow.
- Add larger public datasets only with source, timestamp, fallback, and limitation documentation.
- Add real Slurm/HPC logs only if actual cluster access becomes available.
- Add Spark/Dask or larger-scale data tooling only if the repository gains a real larger-data path.
- Continue keeping claims conservative so the portfolio remains credible for both recruiter and technical review.
