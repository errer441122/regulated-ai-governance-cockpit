from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .data_validation import validate_dataset, write_report
from .drift import load_drift_report


ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT / "evidence-lock" / "results"
ML_ARTIFACTS = ROOT / "ml-baseline" / "artifacts"
PUBLIC_ARTIFACTS = ROOT / "public-risk-ml-lab" / "artifacts"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "missing", "path": str(path.relative_to(ROOT))}
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate() -> dict[str, Any]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    data_quality = validate_dataset()
    write_report(data_quality)
    ml_metrics = _load_json(ML_ARTIFACTS / "metrics.json")
    public_metrics = _load_json(PUBLIC_ARTIFACTS / "metrics.json")
    summary = {
        "dataset": "synthetic regulated risk dataset plus public Wisconsin Diagnostic Breast Cancer lab",
        "model": "Logistic Regression + RandomForest baseline",
        "metrics": {
            "roc_auc": ml_metrics.get("roc_auc"),
            "pr_auc": ml_metrics.get("pr_auc"),
            "f1": ml_metrics.get("f1"),
            "recall": ml_metrics.get("recall"),
            "brier_score": ml_metrics.get("brier_score"),
        },
        "public_risk_lab": {
            "dataset": public_metrics.get("dataset"),
            "selected_model": public_metrics.get("selected_model"),
            "roc_auc": public_metrics.get("roc_auc"),
            "f1": public_metrics.get("f1"),
            "brier_score": public_metrics.get("brier_score"),
        },
        "calibration": "included" if (ML_ARTIFACTS / "calibration.json").exists() else "missing",
        "data_quality": data_quality["status"],
        "drift_check": "included" if load_drift_report().get("status") != "missing" else "missing",
        "api_smoke_test": "run make smoke or python -m src.regulated_ai_governance.api_smoke_test",
        "docker_smoke_test": "documented in evidence/docker-smoke-test.md",
        "limitations": "included",
        "boundary": "Portfolio evidence summary only; no production, legal, credit, or aid-allocation use.",
    }
    path = RESULTS_DIR / "metrics_summary.json"
    path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def main() -> None:
    print(json.dumps(evaluate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
