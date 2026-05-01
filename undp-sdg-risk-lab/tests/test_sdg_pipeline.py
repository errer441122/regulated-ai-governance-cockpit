from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from build_sdg_features import build_features, load_indicator_rows
from run_pipeline import run
from text_mining import load_text_rows, topic_keywords


def test_sdg_features_shape_and_flags():
    scored = build_features(load_indicator_rows())
    assert len(scored) >= 8
    assert all("sdg_risk_score" in row for row in scored)
    assert sum(int(row["capacity_support_flag"]) for row in scored) >= 1


def test_text_mining_returns_keywords():
    topics = topic_keywords(load_text_rows())
    assert len(topics) >= 8
    assert all(row["topic_keywords"] for row in topics)


def test_pipeline_writes_artifacts(tmp_path):
    summary = run(output_dir=tmp_path)
    assert summary["rows"] >= 8
    for name in [
        "sdg_risk_summary.json",
        "sdg_policy_note.md",
        "responsible_data_checklist.md",
        "nlp_topic_summary.csv",
    ]:
        assert (tmp_path / name).exists()
