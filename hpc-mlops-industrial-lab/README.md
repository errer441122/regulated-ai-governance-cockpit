# HPC, MLOps, and Regulated AI Risk Lab

This lab is the technical upgrade for industrial AI, MLOps, and AI Factory screening where the static cockpit is not enough. It is intentionally small, executable, and best framed as BI-REX / industrial AI supplement evidence, not as a credit-risk or public-sector project.

It uses simulated data only.

## What It Demonstrates

- ML training and evaluation with a reproducible binary classifier.
- Text-mining features from workflow notes.
- GIS-lite feature engineering through distance-to-hub calculation.
- SQL feature mart creation with SQLite.
- MQTT/OPC UA-style telemetry payload validation.
- Industrial anomaly score and threshold summary artifact.
- MLOps-style outputs: metrics, predictions, model card, and run manifest.
- HPC readiness evidence through a Slurm batch script.
- Orchestration mapping through lightweight Airflow and Dagster adapters.
- Responsible AI boundary: the model recommends human escalation, it does not automate a decision.

## Why This Exists

The original portfolio was strong on governance and consulting framing but weak on hands-on AI engineering. This folder closes part of that gap without pretending to be a production system.

| Screening signal | Evidence in this lab |
| --- | --- |
| Industrial AI support | telemetry schema validation, anomaly score, threshold summary |
| Data engineering | feature mart, SQL script, reproducible artifacts |
| MLOps support | metrics, predictions, model card, run manifest |
| AI Factory / HPC readiness | Slurm job script, AI workload packaging, reproducible batch run |
| Responsible AI | human escalation target, audit narrative, explicit limits |

## Run Locally

From the repository root:

```bash
python3 hpc-mlops-industrial-lab/src/run_pipeline.py
python3 -m unittest discover hpc-mlops-industrial-lab/tests
```

Outputs are written to `hpc-mlops-industrial-lab/artifacts/` and ignored by git.

Key outputs:

- `artifacts/metrics.json`
- `artifacts/industrial_monitoring_summary.json`
- `artifacts/regulated_feature_mart.sqlite`
- `artifacts/run_manifest.json`
- `data/public_industrial_dataset_manifest.json`
- `demo/telemetry_payload.json`

Fast reviewer route: `docs/reviewer/BI_REX_INDUSTRIAL_AI_ROUTE.md`.
Demo script: `docs/reviewer/BI_REX_DEMO_SCRIPT.md`.

## Reviewer Notes

This is not Spark, MLflow, Kubeflow, Airflow, Dagster, cloud, or HPC production work. It is a compact portfolio simulation that shows the same operating concepts in a way a reviewer can run quickly.

It is also not connected to MQTT brokers, OPC UA servers, MES, SCADA, factory telemetry, or predictive-maintenance datasets. The schema and anomaly score are local engineering evidence only.

The production-equivalent path would be:

- replace SQLite with DuckDB, BigQuery, Snowflake, or lakehouse tables;
- replace the local classifier with scikit-learn, PyTorch, or Spark MLlib;
- register metrics and model versions in MLflow;
- run orchestration through Airflow or Dagster;
- submit training jobs through Slurm on an HPC or GPU partition;
- store artifacts in S3-compatible object storage.
