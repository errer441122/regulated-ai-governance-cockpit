# Public-Sector / SDG Route for UNDP Review

## Problem

Country offices and programme teams need a transparent way to identify where digital public service programmes may require capacity-building support before AI or data-driven tools are piloted.

The project frames the output as a programme-support queue, not an automated decision system.

## Public Indicators Used

- `internet_users_pct`
- `mobile_subscriptions_per_100`
- `gov_effectiveness_score`
- `disaster_risk_index`
- `fragility_flag`
- `data_protection_maturity`
- `ai_readiness_score`
- `case_notes` risk terms for contextual flags

## Data Sources

- Offline reproducible sample: `data/public_development_sample.csv`
- Public refresh path: `data/world_bank_refresh.csv`
- Fetch script: `src/fetch_world_bank_sample.py`

The offline sample keeps CI and reviewer runs reproducible. The refresh path shows how public indicators can be updated when network access is available.

## Stakeholders

- Country office programme team
- Digital transformation lead
- Data governance / privacy reviewer
- Local implementation partner
- Monitoring and evaluation officer
- Human reviewer / escalation owner

## Decision Boundary

The model does not allocate aid, determine eligibility, rank people, automate procurement, or make policy decisions.

It flags programme rows for human-reviewed capacity-support discussion.

## Human Review Checklist

- Is the indicator source current?
- Is the country context interpreted by a local reviewer?
- Are vulnerable groups or accessibility constraints considered?
- Is data protection maturity sufficient for the next implementation step?
- Is the output being used as a briefing aid rather than a decision?
- Is there a clear escalation owner before any AI-enabled pilot?

## SDG / Public-Value Framing

This project is about responsible digital capacity support, not automated public-sector decision-making. It supports digital public infrastructure readiness, trusted data use, capacity building, and safe adoption planning for public-service programmes.

## Reviewer Artifacts

- `M_AND_E_DASHBOARD_SPEC.md`
- `RESPONSIBLE_AI_RISK_REGISTER.md`
- `reports/capacity_building_brief.example.md`
- `grafana/capacity_support_dashboard.json`
- `artifacts/run_manifest.json`
