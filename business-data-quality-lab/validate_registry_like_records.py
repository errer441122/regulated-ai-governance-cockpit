from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "registry_like_sample.csv"
REPORT_PATH = BASE_DIR / "anomaly_report.md"

SAMPLE_ROWS = [
    {"business_id": "IT-0001", "legal_name": "Alfa Servizi SRL", "vat_id": "IT01234567890", "city": "Bologna", "status": "active", "employees": "42"},
    {"business_id": "IT-0002", "legal_name": "Beta Data SPA", "vat_id": "IT09876543210", "city": "Milano", "status": "active", "employees": "120"},
    {"business_id": "IT-0003", "legal_name": "Gamma Labs SRL", "vat_id": "IT00000000000", "city": "", "status": "active", "employees": "-4"},
    {"business_id": "IT-0004", "legal_name": "Delta Mobility SRL", "vat_id": "IT11122233344", "city": "Torino", "status": "inactive", "employees": "18"},
    {"business_id": "IT-0005", "legal_name": "Beta Data S.p.A.", "vat_id": "IT09876543210", "city": "Milan", "status": "active", "employees": "121"},
]


def _ensure_sample() -> None:
    if DATA_PATH.exists():
        return
    with DATA_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SAMPLE_ROWS[0].keys())
        writer.writeheader()
        writer.writerows(SAMPLE_ROWS)


def validate() -> dict[str, object]:
    _ensure_sample()
    rows = list(csv.DictReader(DATA_PATH.open(newline="", encoding="utf-8")))
    anomalies = []
    for row in rows:
        if not row["city"]:
            anomalies.append({"business_id": row["business_id"], "issue": "missing_city"})
        if int(row["employees"]) < 0:
            anomalies.append({"business_id": row["business_id"], "issue": "negative_employee_count"})
        if row["vat_id"] == "IT00000000000":
            anomalies.append({"business_id": row["business_id"], "issue": "placeholder_vat_id"})
    return {"rows": len(rows), "anomalies": anomalies, "status": "review_required" if anomalies else "passed"}


def main() -> None:
    result = validate()
    lines = [
        "# Registry-Like Data Anomaly Report",
        "",
        f"Rows checked: `{result['rows']}`",
        f"Status: `{result['status']}`",
        "",
        "| Business ID | Issue |",
        "| --- | --- |",
    ]
    for item in result["anomalies"]:
        lines.append(f"| {item['business_id']} | {item['issue']} |")
    lines.extend(
        [
            "",
            "Boundary: synthetic registry-like records only; no real CRIF, chamber-of-commerce, or customer data.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (BASE_DIR / "validation_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
