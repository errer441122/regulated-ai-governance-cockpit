from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from pipeline import detect_blockers, readiness_class, readiness_score, validate_schema


def test_readiness_class_thresholds():
    assert readiness_class(4.25) == "controlled_pilot_ready"
    assert readiness_class(3.5) == "prepare_then_pilot"
    assert readiness_class(2.75) == "foundation_work_needed"
    assert readiness_class(2.0) == "not_ready"


def test_blockers_detect_high_sensitivity_weak_governance():
    row = pd.Series(
        {
            "data_sensitivity": "high",
            "data_governance": 2,
            "metadata_quality": 4,
            "owner_named": "yes",
            "agentic_use_approved": "yes",
            "stakeholder_clarity": 4,
        }
    )
    assert "high_sensitivity_weak_governance" in detect_blockers(row)


def test_readiness_score_uses_weighted_dimensions():
    row = pd.Series(
        {
            "metadata_quality": 5,
            "data_governance": 5,
            "stakeholder_clarity": 5,
            "data_engineering_maturity": 5,
            "reporting_value": 5,
            "ai_workload_fit": 5,
        }
    )
    assert readiness_score(row) == 5.0


def test_schema_validation_catches_missing_columns():
    issues = validate_schema(pd.DataFrame({"workflow_id": ["WF-TEST"]}))
    assert issues
    assert "Missing columns" in issues[0]
