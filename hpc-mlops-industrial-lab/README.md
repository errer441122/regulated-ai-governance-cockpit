# HPC, MLOps, and Regulated AI Risk Lab

This lab is the technical upgrade for AI/data internships where the static cockpit is not enough. It is intentionally small, but it is executable and maps to the gaps requested by CRIF, PwC, CINECA, IT4LIA, and BI-REX.

It uses simulated data only.

## What It Demonstrates

- ML training and evaluation with a reproducible binary classifier.
- Text-mining features from workflow notes.
- GIS-lite feature engineering through distance-to-hub calculation.
- SQL feature mart creation with SQLite.
- MLOps-style outputs: metrics, predictions, model card, and run manifest.
- HPC readiness evidence through a Slurm batch script.
- Orchestration mapping through lightweight Airflow and Dagster adapters.
- Responsible AI boundary: the model recommends human escalation, it does not automate a decision.

## Why This Exists

The original portfolio was strong on governance and consulting framing but weak on hands-on AI engineering. This folder closes part of that gap without pretending to be a production system.

| Internship signal | Evidence in this lab |
| --- | --- |
| CRIF ML engineering | Logistic classifier, text features, GIS-lite distance feature, data quality gates |
| PwC Data & AI consulting | Feature mart, metrics, model card, CI-ready reproducibility |
| UNDP responsible AI | Human escalation target, audit narrative, explicit limits |
| CINECA / IT4LIA | Slurm job script, AI workload packaging, reproducible batch run |
| BI-REX | Industrial-style telemetry/failure signals, S3-style artifact layout, monitoring-ready outputs |

## Run Locally

From the repository root:

```bash
python3 hpc-mlops-industrial-lab/src/run_pipeline.py
python3 -m unittest discover hpc-mlops-industrial-lab/tests
```

Outputs are written to `hpc-mlops-industrial-lab/artifacts/` and ignored by git.

## Reviewer Notes

This is not Spark, MLflow, Kubeflow, Airflow, Dagster, cloud, or HPC production work. It is a compact portfolio simulation that shows the same operating concepts in a way a reviewer can run quickly.

The production-equivalent path would be:

- replace SQLite with DuckDB, BigQuery, Snowflake, or lakehouse tables;
- replace the local classifier with scikit-learn, PyTorch, or Spark MLlib;
- register metrics and model versions in MLflow;
- run orchestration through Airflow or Dagster;
- submit training jobs through Slurm on an HPC or GPU partition;
- store artifacts in S3-compatible object storage.
