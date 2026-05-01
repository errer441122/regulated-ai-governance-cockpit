from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT_SCRIPT = ROOT / "scripts" / "build_evidence_report.py"


def build_report() -> Path:
    spec = importlib.util.spec_from_file_location("build_evidence_report", REPORT_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {REPORT_SCRIPT}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_report()


def main() -> None:
    print(build_report())


if __name__ == "__main__":
    main()
