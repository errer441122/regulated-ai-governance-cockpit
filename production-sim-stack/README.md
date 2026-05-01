# Production Simulation Stack

This folder is the local production-simulation layer for CRIF, PwC, UNDP, CINECA/IT4LIA, and BI-REX-style screening.

It does not claim real production infrastructure. It packages the portfolio logic as a production-like simulation with API serving, batch orchestration, artifact tracking, object-storage layout, SQL mart design, monitoring exports, and HPC batch entrypoints.

Architecture and smoke-test boundaries:

- `docs/architecture.md`
- `docs/smoke_test_plan.md`
- `scripts/check_api_contract.py`
- `scripts/smoke_test_local.sh`
- `../README_DEPLOYMENT.md`
- `../render.yaml`

## What This Adds

| Gap | Evidence in this folder |
| --- | --- |
| FastAPI scoring endpoint | `src/api.py`, `/health`, `/metadata`, `/score`, `/docs` |
| Docker path | `Dockerfile`, `docker-compose.yml`, `requirements-api.txt` |
| Render deploy readiness | `../render.yaml`, `../README_DEPLOYMENT.md`, `../evidence/deployment_evidence.md` |
| MLflow-style lifecycle | `src/orchestrate.py`, generated `artifacts/mlflow_run.json` |
| MinIO/S3-style storage | `docker-compose.yml`, generated `artifacts/minio_manifest.json` |
| DuckDB/dbt-style mart | `sql/feature_mart.duckdb.sql` |
| Public-data path for UNDP | `src/fetch_world_bank_sample.py`, `data/public_development_sample.csv` fallback |
| Public-sector programme route | `PUBLIC_SECTOR_SDG_ROUTE.md`, `M_AND_E_DASHBOARD_SPEC.md`, `RESPONSIBLE_AI_RISK_REGISTER.md`, `reports/capacity_building_brief.example.md` |
| Monitoring path | generated Influx line protocol and Grafana dashboard |
| HPC/Slurm path | `slurm/run_capacity_scoring_array.sbatch` |

## Local Validation

From the repository root:

```bash
python -m unittest discover production-sim-stack/tests
python production-sim-stack/src/orchestrate.py
python production-sim-stack/scripts/check_api_contract.py
docker build -t regulated-ai-governance-api:local production-sim-stack
```

Optional service run, if Docker and dependencies are available:

```bash
cd production-sim-stack
docker compose up --build
```

The repository includes a recorded local smoke test from 2026-05-01:

- `../evidence/docker-smoke-test.md`
- `../evidence/docker-smoke-test.json`
- `../evidence/technical-screenshots/docker-api-smoke.png`

That smoke test verified FastAPI, MinIO, MLflow, InfluxDB, and Grafana endpoints from Docker Compose. It is evidence of a production-like simulation run, not a real cloud deployment.

## Cloud Deployment Readiness

The API service is ready for an external Render deploy through the root `render.yaml` Blueprint. The deploy target is only the lightweight FastAPI service, not the full local Docker Compose simulation.

Public API contract:

- `GET /health`
- `GET /metadata`
- `POST /score`
- `POST /score/regulated-workflow`
- `POST /score/capacity-support`
- `GET /docs`
- `GET /openapi.json`

Use `../README_DEPLOYMENT.md` for setup steps and `../evidence/deployment_evidence.md` to record the live URL after deployment.

## Public Dataset Positioning

The included CSV is a small offline fallback with a World Bank/HDX-style schema so tests are reproducible. The production path is `src/fetch_world_bank_sample.py`, which pulls public World Bank indicators when network access is available.

`data/world_bank_refresh.csv` is a small live World Bank API output generated on 2026-05-01 for reviewer credibility. It includes internet-use and mobile-subscription indicators for eight country codes.

Relevant public sources:

- World Bank API: `https://api.worldbank.org/v2/`
- HDX: `https://data.humdata.org/`
- UNDP Sustainable Development Goals context: `https://sdgs.undp.org/`

## Reviewer Boundary

The model is advisory. It flags country-programme rows for capacity-support review at a conservative portfolio threshold of `0.3`. It does not automate aid allocation, eligibility, procurement, legal, or policy decisions.
