import importlib.util
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path


PIPELINE_PATH = Path(__file__).resolve().parents[1] / "src" / "run_pipeline.py"
SPEC = importlib.util.spec_from_file_location("regulated_hpc_pipeline", PIPELINE_PATH)
pipeline = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = pipeline
SPEC.loader.exec_module(pipeline)


class RegulatedHpcPipelineTest(unittest.TestCase):
    def test_text_mining_flags_risk_language(self):
        text = "missing consent complaint with manual override"
        self.assertGreaterEqual(pipeline.count_text_risk_hits(text), 4)

    def test_pipeline_generates_metrics_and_feature_mart(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = pipeline.run_pipeline(output_dir=Path(temp_dir))

            self.assertEqual(result["rows"], 24)
            self.assertGreaterEqual(result["metrics"]["accuracy"], 0.8)
            self.assertGreaterEqual(result["metrics"]["f1"], 0.8)
            self.assertTrue(Path(result["artifacts"]["model_card"]).exists())

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
