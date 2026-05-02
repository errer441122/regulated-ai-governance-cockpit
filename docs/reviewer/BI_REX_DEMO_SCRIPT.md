# BI-REX Industrial AI Demo Script

This is a 60-90 second local demo path for the industrial AI supplement. It uses simulated telemetry-style data and a public predictive-maintenance dataset manifest; it does not connect to factory systems.

## Terminal Demo

1. Run the industrial pipeline:

```bash
python hpc-mlops-industrial-lab/src/run_pipeline.py
```

2. Start the local telemetry API:

```bash
cd hpc-mlops-industrial-lab/src
python -m uvicorn api:app --port 8002
```

3. In another terminal, score the demo payload:

```bash
curl -s -X POST http://127.0.0.1:8002/telemetry/anomaly \
  -H "Content-Type: application/json" \
  --data-binary "@hpc-mlops-industrial-lab/demo/telemetry_payload.json"
```

Expected response shape:

```json
{
  "asset_id": "cnc-07",
  "schema_validation": {
    "valid": true,
    "protocol_style": "mqtt-opcua-telemetry"
  },
  "anomaly_score": 0.6077,
  "alert": 1,
  "decision_boundary": "maintenance triage only; no automated shutdown"
}
```

## What To Show On Screen

- `hpc-mlops-industrial-lab/data/public_industrial_dataset_manifest.json`
- `hpc-mlops-industrial-lab/demo/telemetry_payload.json`
- `hpc-mlops-industrial-lab/artifacts/industrial_monitoring_summary.json`
- `hpc-mlops-industrial-lab/tests/test_pipeline.py`

## Boundary To Say Out Loud

This is telemetry-style engineering evidence, not live industrial integration. The public dataset manifest points to UCI AI4I and NASA C-MAPSS as credible next benchmark paths, while the local payload is simulated and safe to publish.
