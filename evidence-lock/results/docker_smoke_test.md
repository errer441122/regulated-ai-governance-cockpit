# Docker Smoke Test - 2026-05-01

This smoke test was executed locally from `production-sim-stack/` after `docker compose up --build -d`.

| Check | Result |
| --- | --- |
| Compose services | `api`, `mlflow`, `minio`, `influxdb`, and `grafana` containers were running |
| FastAPI health | `{"status":"ok"}` |
| FastAPI scoring | `{"programme_id":"PG-001","country":"Kenya","predicted_capacity_support_probability":0.659,"predicted_capacity_support":1,"decision_boundary":"advisory human-review triage only"}` |
| MinIO health | `HTTP 200 empty body` |
| MLflow health | `OK` |
| InfluxDB health | `{"name":"influxdb", "message":"ready for queries and writes", "status":"pass", "checks":[], "version": "v2.7.12", "commit": "ec9dcde5d6"}` |
| Grafana health | `{
  "database": "ok",
  "version": "11.3.0",
  "commit": "d9455ff7db73b694db7d412e49a68bec767f2b5a"
}` |

Reviewer boundary: this is a production-like simulation, not a real cloud deployment or production MLOps environment.
