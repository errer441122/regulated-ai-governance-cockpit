from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "ml-baseline" / "data" / "simulated_regulated_risk_dataset.csv"
RESULTS_DIR = ROOT / "evidence-lock" / "results"

REQUIRED_COLUMNS = {
    "record_id",
    "sector",
    "region",
    "data_quality_score",
    "financial_signal_score",
    "late_payment_signal",
    "text_risk_score",
    "region_macro_risk",
    "sector_risk_score",
    "human_review_required",
    "target_default_or_escalation",
}


def load_rows(path: Path = DATA_PATH) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate_dataset(path: Path = DATA_PATH) -> dict[str, Any]:
    rows = load_rows(path)
    columns = set(rows[0].keys()) if rows else set()
    missing = sorted(REQUIRED_COLUMNS - columns)
    duplicate_ids = len({row["record_id"] for row in rows}) != len(rows) if rows else False
    numeric_columns = [
        "data_quality_score",
        "financial_signal_score",
        "late_payment_signal",
        "text_risk_score",
        "region_macro_risk",
        "sector_risk_score",
        "human_review_required",
        "target_default_or_escalation",
    ]
    parse_failures: list[str] = []
    for index, row in enumerate(rows, start=2):
        for column in numeric_columns:
            try:
                float(row[column])
            except (KeyError, TypeError, ValueError):
                parse_failures.append(f"row {index}: {column}")

    report = {
        "dataset": str(path.relative_to(ROOT)),
        "rows": len(rows),
        "columns": sorted(columns),
        "missing_required_columns": missing,
        "duplicate_record_ids": duplicate_ids,
        "numeric_parse_failures": parse_failures[:20],
        "status": "passed" if rows and not missing and not duplicate_ids and not parse_failures else "failed",
        "boundary": "Synthetic portfolio dataset validation; not production data-quality certification.",
    }
    return report


def write_report(report: dict[str, Any] | None = None) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = report or validate_dataset()
    path = RESULTS_DIR / "data_validation_report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def main() -> None:
    report = validate_dataset()
    write_report(report)
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
