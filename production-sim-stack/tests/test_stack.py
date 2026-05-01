import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = BASE_DIR / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


pipeline = load_module("production_capacity_pipeline_test", "src/pipeline.py")
orchestrate = load_module("production_capacity_orchestrate_test", "src/orchestrate.py")
api = load_module("production_capacity_api_test", "src/api.py")
ml_model_adapter = load_module("production_capacity_ml_model_adapter_test", "src/ml_model_adapter.py")


class ProductionSimulationStackTest(unittest.TestCase):
    def test_scoring_flags_fragile_capacity_context(self):
        records = pipeline.load_records()
        haiti = next(row for row in records if row["iso3"] == "HTI")
        self.assertGreaterEqual(pipeline.score_record(haiti), 0.5)
        self.assertGreaterEqual(pipeline.count_text_risk_hits(str(haiti["case_notes"])), 3)

    def test_orchestration_writes_lifecycle_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = orchestrate.run(output_dir=Path(temp_dir))
            self.assertEqual(manifest["rows"], 20)
            self.assertGreaterEqual(manifest["metrics"]["accuracy"], 0.8)
            self.assertGreaterEqual(manifest["metrics"]["f1"], 0.8)

            mlflow_payload = json.loads(Path(manifest["artifacts"]["mlflow"]).read_text(encoding="utf-8"))
            self.assertEqual(mlflow_payload["experiment"], "portfolio-production-sim")

            with closing(sqlite3.connect(manifest["artifacts"]["mart"])) as connection:
                count = connection.execute("SELECT COUNT(*) FROM capacity_support_features").fetchone()[0]
            self.assertEqual(count, 20)

    def test_api_scoring_function_is_dependency_light(self):
        payload = pipeline.load_records()[0]
        response = api.score_payload(payload)
        self.assertIn("predicted_capacity_support_probability", response)
        self.assertEqual(response["decision_boundary"], "advisory human-review triage only")

    def test_api_metadata_function_is_dependency_light(self):
        metadata = api.metadata_payload()
        self.assertEqual(metadata["service"], "regulated-ai-governance-api")
        self.assertEqual(metadata["decision_boundary"], "advisory human-review triage only")
        self.assertIn("/score", {endpoint["path"] for endpoint in metadata["endpoints"]})
        self.assertIn("not a production system", metadata["limitations"])

    @unittest.skipIf(api.app is None, "FastAPI is not installed in the local test environment.")
    def test_fastapi_contract_exposes_deploy_endpoints(self):
        from fastapi.testclient import TestClient

        client = TestClient(api.app)
        health = client.get("/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["status"], "ok")

        metadata = client.get("/metadata")
        self.assertEqual(metadata.status_code, 200)
        self.assertEqual(metadata.json()["service"], "regulated-ai-governance-api")

        openapi = client.get("/openapi.json")
        self.assertEqual(openapi.status_code, 200)
        self.assertIn("/score", openapi.json()["paths"])

        payload = {
            "workflow_id": "WF-API-ALIAS",
            "sector": "credit_risk",
            "region": "Lombardy",
            "lat": 45.46,
            "lon": 9.19,
            "data_quality_score": 61,
            "governance_maturity": 2,
            "automation_complexity": 5,
            "stage_age_days": 80,
            "gdpr_sensitive": 1,
            "field_failure_signals": 2,
            "case_notes": "missing consent complaint manual override",
        }
        scored = client.post("/score", json=payload)
        self.assertEqual(scored.status_code, 200)
        self.assertIn("needs_human_escalation_probability", scored.json())

    def test_api_exposes_regulated_workflow_model_adapter(self):
        payload = {
            "workflow_id": "WF-API",
            "sector": "manufacturing",
            "region": "Piedmont",
            "lat": 45.0703,
            "lon": 7.6869,
            "data_quality_score": 62,
            "governance_maturity": 2,
            "automation_complexity": 5,
            "stage_age_days": 88,
            "gdpr_sensitive": 0,
            "field_failure_signals": 3,
            "case_notes": "sensor drift anomaly incomplete maintenance labels",
        }
        response = api.score_regulated_workflow_payload(payload)
        self.assertIn(response["model_source"], {"sklearn_artifact", "transparent_rule_baseline"})
        self.assertIn("needs_human_escalation_probability", response)
        self.assertEqual(response["decision_boundary"], "advisory human-review triage only")

    def test_ml_model_adapter_has_transparent_fallback(self):
        payload = {
            "workflow_id": "WF-ADAPTER",
            "sector": "credit_risk",
            "region": "Sicily",
            "lat": "38.1157",
            "lon": "13.3615",
            "data_quality_score": "58",
            "governance_maturity": "2",
            "automation_complexity": "4",
            "stage_age_days": "74",
            "gdpr_sensitive": "1",
            "field_failure_signals": "2",
            "case_notes": "missing consent complaint manual override debt dispute",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            response = ml_model_adapter.score_regulated_workflow(payload, Path(temp_dir) / "missing.joblib")
        self.assertEqual(response["model_source"], "transparent_rule_baseline")
        self.assertEqual(response["needs_human_escalation"], 1)
        self.assertEqual(response["decision_boundary"], "advisory human-review triage only")


if __name__ == "__main__":
    unittest.main()
