# Industrial AI 5-Minute Route

Use this route for BI-REX or industrial-AI screening. It is a supplement to the main regulated AI cockpit; it should not be framed as credit-risk, UNDP, or employer-specific evidence.

## Open These Files In Order

1. `hpc-mlops-industrial-lab/README.md`
2. `hpc-mlops-industrial-lab/src/run_pipeline.py`
3. `hpc-mlops-industrial-lab/tests/test_pipeline.py`
4. `hpc-mlops-industrial-lab/artifacts/industrial_monitoring_summary.json`
5. `hpc-mlops-industrial-lab/artifacts/metrics.json`
6. `hpc-mlops-industrial-lab/data/public_industrial_dataset_manifest.json`
7. `docs/reviewer/BI_REX_DEMO_SCRIPT.md`
8. `hpc-mlops-industrial-lab/demo/telemetry_payload.json`
9. `production-sim-stack/docs/architecture.md`
10. `production-sim-stack/docker-compose.yml`

## What This Shows

| Signal | Evidence |
| --- | --- |
| Industrial telemetry schema thinking | MQTT/OPC UA-style payload validation in `validate_industrial_message` |
| Anomaly scoring | `industrial_anomaly_score` and threshold summary |
| Feature engineering | text risk hits, distance-to-hub, workflow quality signals |
| Metric output | `artifacts/metrics.json`, `artifacts/industrial_monitoring_summary.json` |
| Data engineering | SQLite feature mart and SQL build script |
| MLOps / packaging | run manifest, model card, Slurm script, production simulation stack |
| Public dataset path | UCI AI4I and NASA C-MAPSS manifest for credible next-step predictive maintenance work |
| Demo path | Local FastAPI `/telemetry/anomaly` endpoint and curl payload |

## Reproduce Locally

```bash
python hpc-mlops-industrial-lab/src/run_pipeline.py
python -m unittest discover hpc-mlops-industrial-lab/tests
```

## Honest Boundary

The data is simulated and telemetry-style. It is not connected to factory equipment, Ducati systems, BI-REX systems, OPC UA servers, MQTT brokers, MES, SCADA, or predictive-maintenance datasets. The goal is to show industrial AI workflow design and testable engineering shape.
