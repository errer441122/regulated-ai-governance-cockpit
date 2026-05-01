# API Deployment Guide

This repository is deployed as a small public FastAPI portfolio service.

Live API:

- Docs: `https://regulated-ai-governance-api.onrender.com/docs`
- Health: `https://regulated-ai-governance-api.onrender.com/health`
- Metadata: `https://regulated-ai-governance-api.onrender.com/metadata`

The deployable service is `production-sim-stack/src/api.py`. It is intentionally scoped as portfolio evidence, not as a production risk, credit, legal, eligibility, or aid-allocation system.

## Public Service Contract

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Service entrypoint with links to docs and metadata |
| `GET` | `/health` | Platform liveness check |
| `GET` | `/metadata` | Scope, boundary, endpoints, and model artifact status |
| `POST` | `/score` | Regulated workflow scoring alias |
| `POST` | `/score/regulated-workflow` | Regulated workflow scoring |
| `POST` | `/score/capacity-support` | Public-sector capacity-support scoring |
| `GET` | `/docs` | OpenAPI Swagger UI |
| `GET` | `/openapi.json` | Machine-readable API contract |

## Render Blueprint

The root `render.yaml` defines one Docker web service:

- service name: `regulated-ai-governance-api`
- root directory: `production-sim-stack`
- health check: `/health`
- auto deploy: only after checks pass
- region: `frankfurt`
- plan: `free`

The Dockerfile installs the lightweight API requirements from `production-sim-stack/requirements-api.txt` and binds Uvicorn to `PORT` when the platform provides it, falling back to `8080` locally.

## Local Verification

From the repository root:

```bash
python -m pip install -r production-sim-stack/requirements-api.txt
python -m unittest discover production-sim-stack/tests
python production-sim-stack/scripts/check_api_contract.py
docker build -t regulated-ai-governance-api:local production-sim-stack
```

Run the API locally:

```bash
cd production-sim-stack
python -m uvicorn src.api:app --host 0.0.0.0 --port 8080
```

Smoke checks:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/metadata
curl http://localhost:8080/openapi.json
```

Example `/score` request:

```bash
curl -X POST http://localhost:8080/score \
  -H "Content-Type: application/json" \
  -d '{"workflow_id":"WF-DEMO-001","sector":"credit_risk","region":"Lombardy","lat":45.46,"lon":9.19,"data_quality_score":61,"governance_maturity":2,"automation_complexity":5,"stage_age_days":80,"gdpr_sensitive":1,"field_failure_signals":2,"case_notes":"missing consent complaint manual override"}'
```

## Render Setup

1. Push this repository to GitHub.
2. In Render, create a Blueprint from the repository.
3. Use the root `render.yaml`.
4. Wait for CI checks and the Docker build.
5. Open the generated `https://<service>.onrender.com` URL.
6. Verify `/health`, `/metadata`, `/docs`, and `/score`.
7. Record the live URL, curl output, and OpenAPI screenshot in `evidence/deployment_evidence.md`.

## Evidence Captured After First Deploy

Recorded in `evidence/deployment_evidence.md`:

- public base URL
- deployment timestamp
- commit SHA
- `/health` response
- `/metadata` response
- `/score` response for the sample payload above
- platform limitation note, especially free-tier sleep/cold-start behavior

## Boundary

This service is valid portfolio evidence for API packaging, Docker deployability, OpenAPI exposure, CI validation, and honest model-risk framing.

It is not evidence of production MLOps, production security review, a real credit model, a real public-sector decision system, or access to any employer or client environment.
