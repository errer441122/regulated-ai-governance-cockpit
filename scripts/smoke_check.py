from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "docs/reviewer/RECRUITER_5_MIN_ROUTE.md",
    "docs/reviewer/CLAIMS_AND_LIMITATIONS.md",
    "ml-baseline/artifacts/metrics.json",
    "ml-baseline/artifacts/model_card.md",
    "undp-sdg-risk-lab/artifacts/sdg_risk_summary.json",
    "hpc-ai-rag-lab/artifacts/retrieval_benchmark.json",
    "production-sim-stack/docs/architecture.md",
]


def main() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    payload = {
        "checked": REQUIRED,
        "missing": missing,
        "boundary": "local artifact presence check only; not production validation",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
