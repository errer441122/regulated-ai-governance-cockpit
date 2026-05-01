from __future__ import annotations

from pathlib import Path
from typing import Any


def write_responsible_checklist(path: Path) -> Path:
    content = """# Responsible Data Checklist

- Privacy: use aggregate programme-level indicators only; avoid personal or household-level targeting.
- Bias: review whether connectivity, education, crisis, and governance indicators under-represent vulnerable groups.
- Data minimization: keep only indicators needed for capacity-support discussion.
- Humanitarian/development sensitivity: require local context review before interpreting high-risk flags.
- Human review: no automated aid, eligibility, procurement, targeting, or policy decisions.
- Limitations: small sample, simplified indicators, no country-office validation, no production monitoring.
- Accountability: document reviewer, data source, date, and reason for any follow-up action.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def write_policy_note(path: Path, scored: list[dict[str, Any]]) -> Path:
    flagged = [row for row in scored if int(row["capacity_support_flag"]) == 1]
    top = sorted(scored, key=lambda row: float(row["sdg_risk_score"]), reverse=True)[:3]
    content = f"""# SDG Capacity-Support Policy Note

## Problem

Programme teams need a transparent way to identify where digital public-service or AI pilots may require capacity-building support before scale-up.

## Data Used

This note uses a small offline public-development-style sample with connectivity, unemployment, climate exposure, education, and governance signals. It is not a real UNDP dataset.

## Findings

- Rows reviewed: {len(scored)}
- Capacity-support flags: {len(flagged)}
- Highest scoring contexts: {", ".join(row["iso3"] for row in top)}

## Responsible Use

The score is a briefing aid for human review. It must not allocate aid, determine eligibility, rank people, automate procurement, or make policy decisions.

## Next Steps

1. Validate indicator freshness and source quality.
2. Ask local programme staff to interpret context.
3. Review privacy and inclusion risks before any AI-enabled pilot.
4. Record human-review outcome and follow-up training needs.

## Limitations

Small sample, simplified indicators, synthetic-style labels, no country-office validation, and no production deployment.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path
