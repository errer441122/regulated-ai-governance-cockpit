from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = BASE_DIR / "artifacts"
REQUIRED = [
    "metrics.json",
    "calibration.json",
    "confusion_matrix.csv",
    "feature_importance.csv",
    "model_card.md",
    "data_card.md",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ARTIFACT_DIR / name).exists()]
    if missing:
        raise SystemExit(f"Missing public-risk artifacts: {missing}")
    metrics = json.loads((ARTIFACT_DIR / "metrics.json").read_text(encoding="utf-8"))
    print(json.dumps({"status": "passed", "metrics": metrics}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
