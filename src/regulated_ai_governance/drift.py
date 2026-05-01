from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DRIFT_PATH = ROOT / "ml-baseline" / "artifacts" / "drift_report.json"


def load_drift_report(path: Path = DRIFT_PATH) -> dict[str, Any]:
    if not path.exists():
        return {
            "status": "missing",
            "path": str(path.relative_to(ROOT)),
            "boundary": "Run python -m src.regulated_ai_governance.train to regenerate drift evidence.",
        }
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    print(json.dumps(load_drift_report(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
