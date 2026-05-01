from pathlib import Path
import sys


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from regulated_risk_ml.config import REQUIRED_COLUMNS
from regulated_risk_ml.data import RiskDatasetBuilder


def test_dataset_builder_generates_expected_schema(tmp_path):
    path = tmp_path / "risk.csv"
    builder = RiskDatasetBuilder(path=path, rows=320)
    rows = builder.generate_rows()
    builder.write_dataset(rows)
    loaded = builder.load_records()

    assert len(loaded) == 320
    assert set(REQUIRED_COLUMNS).issubset(loaded[0])
    assert {row["target_default_or_escalation"] for row in loaded} == {"0", "1"}
