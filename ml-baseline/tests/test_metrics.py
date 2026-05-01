from pathlib import Path
import sys


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from regulated_risk_ml.calibration import CalibrationReporter
from regulated_risk_ml.metrics import ModelEvaluator


def test_metrics_include_required_fields():
    labels = [0, 0, 1, 1]
    probabilities = [0.1, 0.3, 0.7, 0.9]
    metrics = ModelEvaluator().evaluate_probabilities(labels, probabilities)

    for key in ("roc_auc", "pr_auc", "f1", "precision", "recall", "brier_score", "confusion_matrix"):
        assert key in metrics
    assert metrics["f1"] == 1.0


def test_calibration_bins_have_expected_count():
    bins = CalibrationReporter(bins=5).build_bins([0, 1], [0.2, 0.8])
    assert len(bins) == 5
    assert sum(row["rows"] for row in bins) == 2
