# Technical 20-Minute Route

Use this route to verify the repository as a local, offline-first regulated AI/ML engineering simulation. The goal is not enterprise scale; it is reproducible evidence for internship screening.

## 1. Validate The Existing Cockpit And Labs

```bash
npm test
```

This validates the static cockpit data and the existing Python unittest suites for `hpc-mlops-industrial-lab/` and `production-sim-stack/`.

## 2. Run The Credit-Risk Lab

```bash
python -m pip install -r credit-risk-model-risk-lab/requirements.txt
python credit-risk-model-risk-lab/src/evaluate.py
python -m pytest -q credit-risk-model-risk-lab/tests
```

Inspect:

- `credit-risk-model-risk-lab/src/`
- `credit-risk-model-risk-lab/reports/evaluation_metrics.json`
- `credit-risk-model-risk-lab/reports/validation_report.md`
- `credit-risk-model-risk-lab/reports/model_card.md`
- `credit-risk-model-risk-lab/reports/feature_importance.csv`
- `docs/reviewer/CRIF_5_MIN_ROUTE.md`

## 3. Verify The Orchestration Path

```bash
python orchestration/local_orchestrator.py
```

This is a Dagster-equivalent local decomposition. It calls validation/training/report paths; it is not a real Dagster, Airflow, or cloud deployment.

## 4. Review Public-Data / SDG Evidence

```bash
python undp-sdg-risk-lab/src/run_pipeline.py
python -m pytest -q undp-sdg-risk-lab/tests
```

Inspect:

- `undp-sdg-risk-lab/artifacts/sdg_policy_note.md`
- `undp-sdg-risk-lab/artifacts/responsible_data_checklist.md`
- `undp-sdg-risk-lab/artifacts/nlp_topic_summary.csv`

## 5. Review AI Factory / Governance-RAG Evidence

```bash
python hpc-ai-rag-lab/src/benchmark.py
python -m pytest -q hpc-ai-rag-lab/tests
```

Inspect:

- `hpc-ai-rag-lab/artifacts/retrieval_benchmark.json`
- `hpc-ai-rag-lab/data/source_manifest.json`
- `hpc-ai-rag-lab/src/api.py`
- `hpc-ai-rag-lab/slurm/run_rag_benchmark.sbatch`
- `hpc-ai-rag-lab/apptainer/Apptainer.def`
- `ai-factory-workload-pack/`

The RAG benchmark includes adversarial and out-of-scope questions. Review `documented_failures`, `grounding_coverage`, and `mean_hallucination_risk_score`; perfect accuracy is not the goal.

## 6. Review Production Simulation Boundaries

Inspect:

- `production-sim-stack/docs/architecture.md`
- `production-sim-stack/docs/smoke_test_plan.md`
- `production-sim-stack/scripts/check_api_contract.py`
- `scripts/smoke_check.py`

The stack is a local simulation with FastAPI-compatible scoring functions, Docker Compose, MLflow-like metadata, MinIO-like manifest, SQL mart, Influx/Grafana-style artifacts, and Slurm packaging. It is not a real cloud deployment.

## Known Honest Limits

- Synthetic and public-development-style sample data only.
- No real employer, client, customer, CINECA, IT4LIA, UNDP, CRIF, PwC, BI-REX, or Ducati data.
- No production security review, model governance approval, cloud deployment, or real Slurm execution.
- Model metrics are portfolio simulation metrics and should not be represented as production validation.
