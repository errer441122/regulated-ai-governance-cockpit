from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from validate_dataset import DATA_PATH, REPORTS_DIR, classify_readiness, readiness_score


LOG_PATH = REPORTS_DIR / "agent_run_log.jsonl"


def slug(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")


def load_approved_row(organization: str) -> pd.Series:
    df = pd.read_csv(DATA_PATH)
    match = df[df["organization"].str.lower() == organization.lower()]
    if match.empty:
        available = ", ".join(sorted(df["organization"].tolist()))
        raise ValueError(f"Organization not found. Available options: {available}")

    row = match.iloc[0]
    if str(row["approved_for_brief"]).lower() != "yes":
        raise ValueError("This row is not approved for brief generation.")

    return row


def build_brief(row: pd.Series, reviewer: str) -> str:
    score = readiness_score(row)
    readiness_class = classify_readiness(score)

    return f"""# Human-Reviewed Agentic Brief Draft

Organization: {row['organization']}
Sector: {row['sector']}
Use case: {row['use_case']}
Generated at: {datetime.now(timezone.utc).isoformat()}
Reviewer required: {reviewer}

## Approved Inputs

- Data source: {row['data_source']}
- Data sensitivity: {row['data_sensitivity']}
- Criticality: {row['criticality']}
- Estimated users: {row['estimated_users']}
- Approved for brief: {row['approved_for_brief']}

## Readiness Assessment

- Readiness score: {score} / 5
- Readiness class: {readiness_class}
- Metadata quality: {row['metadata_quality']} / 5
- Process maturity: {row['process_maturity']} / 5
- Stakeholder clarity: {row['stakeholder_clarity']} / 5
- Automation potential: {row['automation_potential']} / 5
- AI governance readiness: {row['ai_governance_readiness']} / 5

## Draft Recommendation

This workflow should be treated as a controlled AI/data implementation candidate, not as an automated decision system. The next step is to confirm source ownership, metadata completeness, privacy boundaries, and the human review owner before any pilot.

## Human Review Checklist

- Confirm the approved data source is current.
- Confirm the use case is described at workflow level, not individual-person level.
- Confirm sensitive data is minimized or aggregated before any AI-assisted step.
- Confirm the reviewer and escalation path are named.
- Confirm the pilot metric and stopping condition are documented.

Status: REQUIRES HUMAN REVIEW BEFORE USE
"""


def write_log(row: pd.Series, output_path: Path, reviewer: str) -> None:
    LOG_PATH.parent.mkdir(exist_ok=True)
    event = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "event": "brief_generated",
        "organization": row["organization"],
        "use_case": row["use_case"],
        "approved_for_brief": row["approved_for_brief"],
        "reviewer": reviewer,
        "output_path": str(output_path.relative_to(REPORTS_DIR.parent)),
        "human_review_required": True,
    }
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a controlled, human-reviewed agentic brief draft.")
    parser.add_argument("--organization", required=True, help="Organization name from the approved dataset.")
    parser.add_argument("--reviewer", required=True, help="Human reviewer name or role.")
    args = parser.parse_args()

    REPORTS_DIR.mkdir(exist_ok=True)
    row = load_approved_row(args.organization)
    brief = build_brief(row, args.reviewer)
    output_path = REPORTS_DIR / f"brief_{slug(row['organization'])}.md"
    output_path.write_text(brief, encoding="utf-8")
    write_log(row, output_path, args.reviewer)

    print(f"Brief written to {output_path}")
    print("Status: REQUIRES HUMAN REVIEW BEFORE USE")


if __name__ == "__main__":
    main()
