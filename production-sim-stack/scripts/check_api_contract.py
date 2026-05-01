from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
API_PATH = BASE_DIR / "src" / "api.py"


def load_api():
    spec = importlib.util.spec_from_file_location("production_sim_api_contract", API_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load production-sim-stack/src/api.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    api = load_api()
    capacity_payload = api.pipeline.load_records()[0]
    capacity = api.score_payload(capacity_payload)
    metadata = api.metadata_payload()
    regulated = api.score_regulated_workflow_payload(
        {
            "workflow_id": "WF-SMOKE",
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
    )
    assert capacity["decision_boundary"] == "advisory human-review triage only"
    assert regulated["decision_boundary"] == "advisory human-review triage only"
    assert metadata["service"] == "regulated-ai-governance-api"
    assert "/score" in {endpoint["path"] for endpoint in metadata["endpoints"]}
    assert "needs_human_escalation_probability" in regulated
    print(
        json.dumps(
            {"capacity_support": capacity, "metadata": metadata, "regulated_workflow": regulated},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
