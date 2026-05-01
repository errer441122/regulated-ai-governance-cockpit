# Smoke Test Plan

This plan separates what can be tested locally from what remains documentation-only.

## Planned Checks

| Check | Command or artifact | Expected result |
| --- | --- | --- |
| Python scoring functions | `python production-sim-stack/scripts/check_api_contract.py` | API contract payloads return advisory responses. |
| Production simulation pipeline | `python production-sim-stack/src/orchestrate.py` | Artifacts written under `production-sim-stack/artifacts/`. |
| Risk ML model fallback | `python -m pytest -q production-sim-stack/tests` | Missing model path falls back to transparent rules. |
| Docker Compose stack | `production-sim-stack/scripts/smoke_test_local.sh` | Optional local service checks if Docker is available. |
| Top-level artifact check | `python scripts/smoke_check.py` | Key files/artifacts exist after local runs. |

## Executed Checks In This Repository

Recorded local Docker evidence from 2026-05-01:

- `evidence/docker-smoke-test.md`
- `evidence/docker-smoke-test.json`
- `evidence/technical-screenshots/docker-api-smoke.png`

This recorded smoke test is evidence of a local production-like simulation run, not a cloud deployment.

## Not Executed By Default

- Real cloud deployment.
- Real MLflow server registration.
- Real MinIO upload with credentials.
- Real InfluxDB/Grafana production monitoring.
- Real Slurm/HPC job submission.
- Real CINECA/IT4LIA/BI-REX infrastructure execution.

## Boundary

All checks support reviewer confidence in local reproducibility. They do not certify production readiness.
