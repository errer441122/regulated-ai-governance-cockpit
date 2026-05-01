# Deployment Evidence

Status: live public Render deployment verified.

## Current Evidence

| Evidence item | Status | File |
| --- | --- | --- |
| FastAPI-compatible service | Live | `production-sim-stack/src/api.py` |
| Health endpoint | Live | `https://regulated-ai-governance-api.onrender.com/health` |
| Metadata endpoint | Live | `https://regulated-ai-governance-api.onrender.com/metadata` |
| Score endpoint | Live | `https://regulated-ai-governance-api.onrender.com/score` |
| OpenAPI contract | Live | `https://regulated-ai-governance-api.onrender.com/openapi.json` and `https://regulated-ai-governance-api.onrender.com/docs` |
| Docker image path | Ready | `production-sim-stack/Dockerfile` |
| Render Blueprint | Ready | `render.yaml` |
| API contract tests | Ready | `production-sim-stack/tests/test_stack.py` |

## Live Deployment Record

| Field | Value |
| --- | --- |
| Public base URL | `https://regulated-ai-governance-api.onrender.com` |
| Platform | Render |
| Service name | `regulated-ai-governance-api` |
| Verification timestamp UTC | `2026-05-01T21:55:44Z` |
| Commit SHA | `34328098a292626881fe53d6fe1ba9fff141551c` |
| Health check result | HTTP 200, `{"status":"ok"}` |
| Metadata check result | HTTP 200, service `regulated-ai-governance-api`, version `1.1.0` |
| OpenAPI check result | HTTP 200, 5341-byte `/openapi.json`; `/docs` HTTP 200 |
| Score check result | HTTP 200 on `POST /score` sample payload |
| Runtime model note | Live container uses `transparent_rule_baseline` fallback because optional `ml-baseline/artifacts/model.joblib` is not present in the Render Docker context |
| Free-tier limitation note | Render free-tier services may sleep and cold-start; this is portfolio execution evidence, not production uptime evidence |

## Curl Evidence

```bash
export LIVE_API_URL="https://regulated-ai-governance-api.onrender.com"
curl "$LIVE_API_URL/health"
curl "$LIVE_API_URL/metadata"
curl "$LIVE_API_URL/openapi.json"
curl -X POST "$LIVE_API_URL/score" \
  -H "Content-Type: application/json" \
  -d '{"workflow_id":"WF-DEMO-001","sector":"credit_risk","region":"Lombardy","lat":45.46,"lon":9.19,"data_quality_score":61,"governance_maturity":2,"automation_complexity":5,"stage_age_days":80,"gdpr_sensitive":1,"field_failure_signals":2,"case_notes":"missing consent complaint manual override"}'
```

Verified responses:

```json
{"status":"ok"}
```

```json
{
  "service": "regulated-ai-governance-api",
  "version": "1.1.0",
  "runtime": "FastAPI-compatible Docker service",
  "project_scope": "portfolio production-simulation evidence",
  "decision_boundary": "advisory human-review triage only"
}
```

```json
{
  "workflow_id": "WF-DEMO-001",
  "model_source": "transparent_rule_baseline",
  "needs_human_escalation_probability": 0.78,
  "needs_human_escalation": 1,
  "decision_boundary": "advisory human-review triage only"
}
```

## Boundary Statement

The deployed API should be described as a public portfolio proof-of-execution for FastAPI, Docker, Render, CI, OpenAPI, and model-risk documentation.

Do not describe it as a production deployment, production credit model, legal compliance system, automated decision system, or employer/client environment.
