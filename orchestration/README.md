# Local Orchestration Path

This folder provides a Dagster-equivalent local orchestration sketch for CRIF/PwC-style review. It decomposes the repository into repeatable assets without claiming a real Dagster, Airflow, cloud, or production deployment.

## What It Runs

`local_orchestrator.py` runs:

1. static cockpit data validation through `npm run test:node`;
2. Risk ML Lab training through `python ml-baseline/train_model.py`;
3. existing production simulation through `python production-sim-stack/src/orchestrate.py`;
4. UNDP SDG lab through `python undp-sdg-risk-lab/src/run_pipeline.py` when present;
5. HPC/RAG benchmark through `python hpc-ai-rag-lab/src/benchmark.py --quick` when present.

It writes `orchestration/run_manifest.json`.

## Run

```bash
python orchestration/local_orchestrator.py
```

## Boundary

This is not a Dagster, Airflow, Kubernetes, cloud, or production scheduler deployment. It is a local reviewer artifact that shows pipeline decomposition and command reproducibility.
