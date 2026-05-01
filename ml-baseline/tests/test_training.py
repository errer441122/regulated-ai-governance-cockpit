from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from train_model import train


def test_training_writes_required_artifacts(tmp_path):
    result = train(output_dir=tmp_path)

    assert result["rows"] >= 300
    assert result["metrics"]["roc_auc"] >= 0.75
    for name in [
        "metrics.json",
        "calibration.json",
        "confusion_matrix.csv",
        "feature_importance.csv",
        "drift_report.json",
        "model_card.md",
    ]:
        assert (tmp_path / name).exists()
