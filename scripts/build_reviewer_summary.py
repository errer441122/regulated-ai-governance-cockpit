from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "reviewer" / "REVIEWER_SUMMARY.md"


def main() -> None:
    sections = [
        "# Reviewer Summary",
        "",
        f"Generated at UTC: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "## Start Here",
        "",
        "- `docs/reviewer/RECRUITER_5_MIN_ROUTE.md`",
        "- `docs/reviewer/TECHNICAL_20_MIN_ROUTE.md`",
        "- `docs/reviewer/CLAIMS_AND_LIMITATIONS.md`",
        "- `docs/reviewer/COMPANY_FIT_MATRIX.md`",
        "- `docs/reviewer/PULL_REQUEST_DESCRIPTION.md`",
        "",
        "## Executable Commands",
        "",
        "```bash",
        "npm test",
        "python -m pytest -q",
        "python ml-baseline/train_model.py",
        "python orchestration/local_orchestrator.py",
        "python scripts/smoke_check.py",
        "```",
        "",
        "## Boundary",
        "",
        "Simulation only: no production deployment, no real employer/company data, no real cloud run, and no real Slurm/HPC execution.",
    ]
    OUTPUT.write_text("\n".join(sections) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
