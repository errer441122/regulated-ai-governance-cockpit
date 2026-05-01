from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path(__file__).resolve().parent / "run_manifest.json"


def run_step(name: str, command: list[str], required: bool = True) -> dict[str, object]:
    executable = shutil.which(command[0]) or command[0]
    resolved_command = [executable, *command[1:]]
    completed = subprocess.run(resolved_command, cwd=REPO_ROOT, text=True, capture_output=True)
    status = "passed" if completed.returncode == 0 else "failed"
    if required and completed.returncode != 0:
        raise RuntimeError(
            f"{name} failed with exit code {completed.returncode}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return {
        "name": name,
        "command": " ".join(command),
        "status": status,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout.strip().splitlines()[-5:],
        "stderr_tail": completed.stderr.strip().splitlines()[-5:],
        "required": required,
    }


def main() -> None:
    steps = [
        ("static_data_validation", ["npm", "run", "test:node"], True),
        ("risk_ml_training", [sys.executable, "ml-baseline/train_model.py"], True),
        ("production_sim_orchestration", [sys.executable, "production-sim-stack/src/orchestrate.py"], True),
        ("undp_sdg_pipeline", [sys.executable, "undp-sdg-risk-lab/src/run_pipeline.py"], True),
        ("hpc_rag_quick_benchmark", [sys.executable, "hpc-ai-rag-lab/src/benchmark.py", "--quick"], True),
    ]
    results = [run_step(name, command, required) for name, command, required in steps]
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "boundary": "local-only orchestration simulation; not a Dagster/Airflow/cloud deployment",
        "steps": results,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Local orchestration completed: steps={len(results)} manifest={MANIFEST_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
