from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline import REPORTS_DIR, load_data, readiness_class, readiness_score, detect_blockers


def build_brief(row, reviewer: str) -> str:
    score = readiness_score(row)
    blockers = detect_blockers(row)
    blocker_text = ", ".join(blockers) if blockers else "None"

    return f"""# Agentic Workflow Brief Draft

Workflow ID: {row['workflow_id']}
Organization: {row['organization']}
Sector: {row['sector']}
Domain: {row['domain']}
Use case: {row['use_case']}
Generated at: {datetime.now(timezone.utc).isoformat()}
Reviewer required: {reviewer}

## Approved Data Context

- Source: {row['data_source']}
- Sensitivity: {row['data_sensitivity']}
- Estimated users: {row['estimated_users']}
- Owner named: {row['owner_named']}
- Agentic use approved: {row['agentic_use_approved']}

## Readiness

- Score: {score} / 5
- Class: {readiness_class(score)}
- Blockers: {blocker_text}

## Recommendation

This workflow can move forward only if blockers are resolved and the named human reviewer confirms the data source, privacy boundary, pilot metric, and escalation path.

## Human Review Checklist

- Data owner confirmed.
- Source fields documented.
- Sensitive data minimized or aggregated.
- Agent output treated as draft support, not a decision.
- Pilot success metric and stopping condition defined.
- Escalation path documented for privacy, compliance, or safety issues.

Status: REQUIRES HUMAN REVIEW BEFORE USE
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a human-reviewed agentic workflow brief.")
    parser.add_argument("--workflow-id", required=True)
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()

    df = load_data()
    match = df[df["workflow_id"] == args.workflow_id]
    if match.empty:
        raise SystemExit(f"Unknown workflow id: {args.workflow_id}")

    row = match.iloc[0]
    REPORTS_DIR.mkdir(exist_ok=True)
    output = REPORTS_DIR / f"agentic_brief_{args.workflow_id.lower()}.md"
    output.write_text(build_brief(row, args.reviewer), encoding="utf-8")

    log_event = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "event": "agentic_brief_generated",
        "workflow_id": args.workflow_id,
        "organization": row["organization"],
        "reviewer": args.reviewer,
        "human_review_required": True,
    }
    with (REPORTS_DIR / "agentic_audit_log.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(log_event) + "\n")

    print(f"Brief written to {output}")
    print("Status: REQUIRES HUMAN REVIEW BEFORE USE")


if __name__ == "__main__":
    main()
