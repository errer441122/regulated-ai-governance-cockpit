from __future__ import annotations

import json
from pathlib import Path

from .api import smoke_test


ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT / "evidence-lock" / "results"


def run() -> dict[str, object]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    terminal_dir = RESULTS_DIR / "terminal_logs"
    terminal_dir.mkdir(parents=True, exist_ok=True)
    payload = smoke_test()
    status = payload["health"]["status"]
    probability = payload["score"]["predicted_review_escalation_probability"]
    md = (
        "# API Smoke Test\n\n"
        "| Check | Result |\n"
        "| --- | --- |\n"
        f"| Health | `{status}` |\n"
        f"| Score probability | `{probability}` |\n"
        "| Boundary | `advisory human-review triage only` |\n"
    )
    (RESULTS_DIR / "api_smoke_test.md").write_text(md, encoding="utf-8")
    (terminal_dir / "api_smoke_test.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return payload


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
