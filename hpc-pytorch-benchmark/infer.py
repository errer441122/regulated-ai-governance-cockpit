from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_PATH = BASE_DIR / "artifacts" / "cpu_benchmark.json"


def main() -> None:
    if not ARTIFACT_PATH.exists():
        from benchmark import run

        run(quick=True)
    payload = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "status": "passed",
                "backend": payload["backend"],
                "inference_latency_ms": payload["inference_latency_ms"],
                "boundary": payload["boundary"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
