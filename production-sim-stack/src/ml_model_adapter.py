from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
ML_BASELINE_DIR = REPO_ROOT / "ml-baseline"
ML_SRC_DIR = ML_BASELINE_DIR / "src"
MODEL_ARTIFACT_PATH = ML_BASELINE_DIR / "artifacts" / "model.joblib"

if str(ML_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(ML_SRC_DIR))

try:
    from regulated_risk_ml.api_adapter import score_payload
except ModuleNotFoundError as exc:  # pragma: no cover - defensive fallback for incomplete checkouts
    score_payload = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


def model_artifact_status(model_path: Path = MODEL_ARTIFACT_PATH) -> dict[str, Any]:
    try:
        display_path = str(model_path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        display_path = str(model_path)
    return {
        "path": display_path,
        "exists": model_path.exists(),
        "fallback": "transparent_rule_baseline",
    }


def score_regulated_workflow(payload: dict[str, Any], model_path: Path = MODEL_ARTIFACT_PATH) -> dict[str, Any]:
    """Score regulated workflow payloads through the Risk ML Lab when available."""
    if score_payload is None:
        return {
            "workflow_id": payload.get("workflow_id", "unknown"),
            "model_source": "transparent_rule_baseline",
            "needs_human_escalation_probability": 0.78,
            "needs_human_escalation": 1,
            "artifact_status": model_artifact_status(model_path),
            "model_load_error": IMPORT_ERROR.__class__.__name__ if IMPORT_ERROR else "ModuleNotFoundError",
            "decision_boundary": "advisory human-review triage only",
        }
    result = score_payload(payload, model_path=model_path)
    result["artifact_status"] = model_artifact_status(model_path)
    return result
