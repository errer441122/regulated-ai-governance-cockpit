from __future__ import annotations

import csv
import json
from difflib import SequenceMatcher
from pathlib import Path

from validate_registry_like_records import DATA_PATH, _ensure_sample


BASE_DIR = Path(__file__).resolve().parent
WORKFLOW_PATH = BASE_DIR / "correction_workflow.md"


def detect_duplicates() -> dict[str, object]:
    _ensure_sample()
    rows = list(csv.DictReader(DATA_PATH.open(newline="", encoding="utf-8")))
    duplicate_candidates = []
    for left_index, left in enumerate(rows):
        for right in rows[left_index + 1 :]:
            same_vat = left["vat_id"] == right["vat_id"]
            name_similarity = SequenceMatcher(None, left["legal_name"].lower(), right["legal_name"].lower()).ratio()
            if same_vat or name_similarity >= 0.82:
                duplicate_candidates.append(
                    {
                        "left_business_id": left["business_id"],
                        "right_business_id": right["business_id"],
                        "same_vat": same_vat,
                        "name_similarity": round(name_similarity, 3),
                        "recommended_action": "human_review_merge_or_confirm",
                    }
                )
    return {"duplicate_candidates": duplicate_candidates, "status": "review_required" if duplicate_candidates else "passed"}


def main() -> None:
    result = detect_duplicates()
    lines = [
        "# Correction Workflow",
        "",
        "1. Validate required fields and numeric ranges.",
        "2. Flag placeholder identifiers, missing locations, and impossible counts.",
        "3. Detect duplicate candidates by VAT match and legal-name similarity.",
        "4. Route candidates to human review before merge, correction, or external confirmation.",
        "5. Preserve audit notes for every accepted or rejected correction.",
        "",
        "## Duplicate Candidates",
        "",
        "| Left ID | Right ID | Same VAT | Name Similarity | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in result["duplicate_candidates"]:
        lines.append(
            f"| {item['left_business_id']} | {item['right_business_id']} | "
            f"{item['same_vat']} | {item['name_similarity']} | {item['recommended_action']} |"
        )
    lines.extend(
        [
            "",
            "Boundary: synthetic registry-like records only; no automated legal, credit, or official register update.",
        ]
    )
    WORKFLOW_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (BASE_DIR / "duplicate_detection_summary.json").write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
