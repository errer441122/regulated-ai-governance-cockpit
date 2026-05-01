# Production Simulation Architecture

This architecture describes a local production-like simulation. It is not a real cloud deployment, not production MLOps, and not a security-reviewed system.

## Components

| Component | Repository artifact | Role |
| --- | --- | --- |
| FastAPI-compatible scoring | `production-sim-stack/src/api.py` | Defines `/health`, `/score/capacity-support`, and `/score/regulated-workflow` when FastAPI is installed; exposes dependency-light scoring functions for tests. |
| Risk ML adapter | `production-sim-stack/src/ml_model_adapter.py` | Loads `ml-baseline/artifacts/model.joblib` when available and falls back to transparent rules. |
| Public-data scoring pipeline | `production-sim-stack/src/pipeline.py` | Scores public-development-style capacity-support rows. |
| Local orchestration | `production-sim-stack/src/orchestrate.py` | Writes predictions, SQLite feature mart, monitoring line protocol, MLflow-like metadata, MinIO-like manifest, and model card JSON. |
| DuckDB/SQL mart | `production-sim-stack/sql/feature_mart.duckdb.sql` | Documents mart-style analytic views for reviewer inspection. |
| Docker Compose | `production-sim-stack/docker-compose.yml` | Optional local service bundle for API, MLflow-like, MinIO-like, InfluxDB, and Grafana components. |
| Monitoring artifacts | `production-sim-stack/grafana/`, `production-sim-stack/artifacts/capacity_alerts_influx.lp` | Dashboard JSON and line protocol generated for local simulation. |
| Slurm packaging | `production-sim-stack/slurm/run_capacity_scoring_array.sbatch` | HPC-ready batch packaging only; not executed on a real cluster. |

## Data Flow

1. Offline public-development sample is loaded from `data/public_development_sample.csv`.
2. `pipeline.py` computes transparent capacity-support scores.
3. `orchestrate.py` writes CSV predictions, SQLite feature mart, monitoring output, lifecycle metadata, and model-card JSON.
4. `api.py` exposes the scoring logic through functions and optional FastAPI endpoints.
5. `ml_model_adapter.py` bridges the CRIF/PwC Risk ML Lab into the production simulation for regulated workflow scoring.

## Failure Modes

- Missing optional FastAPI dependency: tests still use plain Python scoring functions.
- Missing `model.joblib`: adapter falls back to transparent rule baseline.
- Missing Docker: local scripts and tests still run without containers.
- Missing network: public-development sample remains offline-first.
- Missing Slurm: `.sbatch` files remain packaging artifacts only.

## Security Limitations

- No authentication or authorization.
- No secrets management.
- No encrypted storage or transport controls.
- No production logging, monitoring, incident response, or model governance workflow.
- No privacy impact assessment or legal compliance certification.

## What Real Production Would Require

- Approved data sources and data protection assessment.
- Authentication, authorization, secrets management, and audit logging.
- Model registry, model versioning, monitoring, rollback, and human-review workflow.
- Cloud or HPC infrastructure review, network controls, container hardening, and vulnerability management.
- Legal, fairness, and governance review before any regulated use.
