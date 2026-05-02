import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path


PIPELINE_PATH = Path(__file__).resolve().parents[1] / "src" / "run_pipeline.py"
API_PATH = Path(__file__).resolve().parents[1] / "src" / "api.py"
DATASET_MANIFEST_PATH = Path(__file__).resolve().parents[1] / "data" / "public_industrial_dataset_manifest.json"
SPEC = importlib.util.spec_from_file_location("regulated_hpc_pipeline", PIPELINE_PATH)
pipeline = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = pipeline
SPEC.loader.exec_module(pipeline)

API_SPEC = importlib.util.spec_from_file_location("regulated_hpc_industrial_api", API_PATH)
industrial_api = importlib.util.module_from_spec(API_SPEC)
assert API_SPEC.loader is not None
sys.modules[API_SPEC.name] = industrial_api
API_SPEC.loader.exec_module(industrial_api)


class RegulatedHpcPipelineTest(unittest.TestCase):
    def test_text_mining_flags_risk_language(self):
        text = "missing consent complaint with manual override"
        self.assertGreaterEqual(pipeline.count_text_risk_hits(text), 4)

    def test_industrial_message_schema_accepts_mqtt_opcua_style_payload(self):
        payload = {
            "topic": "factory/line-a/cnc-07/telemetry",
            "asset_id": "cnc-07",
            "timestamp_utc": "2026-05-02T10:15:00Z",
            "temperature_c": 82.4,
            "vibration_mm_s": 6.8,
            "cycle_time_ms": 1320,
            "quality_flag": "warning",
        }

        result = pipeline.validate_industrial_message(payload)

        self.assertTrue(result["valid"])
        self.assertEqual(result["asset_id"], "cnc-07")
        self.assertEqual(result["protocol_style"], "mqtt-opcua-telemetry")

    def test_industrial_anomaly_score_and_threshold_summary_are_monotonic(self):
        normal = pipeline.industrial_anomaly_score(
            {"temperature_c": 55.0, "vibration_mm_s": 2.0, "cycle_time_ms": 900, "quality_flag": "ok"}
        )
        warning = pipeline.industrial_anomaly_score(
            {"temperature_c": 87.0, "vibration_mm_s": 7.2, "cycle_time_ms": 1420, "quality_flag": "warning"}
        )
        summary = pipeline.threshold_operating_summary([normal, warning], threshold=0.5)

        self.assertLess(normal, warning)
        self.assertEqual(summary["alerts"], 1)
        self.assertEqual(summary["threshold"], 0.5)

    def test_industrial_api_payload_returns_contract_and_alert(self):
        payload = json.loads(
            (Path(__file__).resolve().parents[1] / "demo" / "telemetry_payload.json").read_text(encoding="utf-8")
        )

        response = industrial_api.score_telemetry_payload(payload)

        self.assertEqual(response["asset_id"], payload["asset_id"])
        self.assertTrue(response["schema_validation"]["valid"])
        self.assertGreaterEqual(response["anomaly_score"], 0.5)
        self.assertEqual(response["alert"], 1)
        self.assertEqual(response["decision_boundary"], "maintenance triage only; no automated shutdown")

    def test_public_industrial_dataset_manifest_lists_predictive_maintenance_sources(self):
        manifest = json.loads(DATASET_MANIFEST_PATH.read_text(encoding="utf-8"))
        ids = {row["id"] for row in manifest}

        self.assertIn("uci-ai4i-2020", ids)
        self.assertIn("nasa-cmapss", ids)
        self.assertTrue(all(row["url"].startswith("https://") for row in manifest))

    def test_pipeline_generates_metrics_and_feature_mart(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = pipeline.run_pipeline(output_dir=Path(temp_dir))

            self.assertEqual(result["rows"], 24)
            self.assertGreaterEqual(result["metrics"]["accuracy"], 0.8)
            self.assertGreaterEqual(result["metrics"]["f1"], 0.8)
            self.assertTrue(Path(result["artifacts"]["model_card"]).exists())
            self.assertTrue(Path(result["artifacts"]["industrial_monitoring"]).exists())

            with closing(sqlite3.connect(result["mart"])) as connection:
                row_count = connection.execute(
                    "SELECT COUNT(*) FROM regulated_workflow_features"
                ).fetchone()[0]
                high_risk_count = connection.execute(
                    """
                    SELECT COUNT(*)
                    FROM regulated_workflow_features
                    WHERE predicted_escalation_probability >= 0.5
                    """
                ).fetchone()[0]

            self.assertEqual(row_count, 24)
            self.assertGreaterEqual(high_risk_count, 8)


if __name__ == "__main__":
    unittest.main()
