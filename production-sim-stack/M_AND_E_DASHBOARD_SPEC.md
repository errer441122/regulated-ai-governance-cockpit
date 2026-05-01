# Monitoring & Evaluation Dashboard Spec

## Users

- Programme officer
- Digital transformation advisor
- Monitoring and evaluation analyst
- Data governance reviewer
- Local implementation partner

## Core Metrics

- `capacity_support_flag_count`
- `average_ai_readiness_score`
- `low_connectivity_programme_count`
- `weak_data_protection_count`
- `high_disaster_risk_count`
- `human_review_completion_rate`
- `training_action_completion_rate`
- `indicator_refresh_age_days`

## Views

1. Country/programme overview
2. Indicator quality and data freshness
3. Capacity-support queue
4. Human-review status
5. Training and follow-up actions

## Governance Controls

- No individual-level targeting
- Aggregate programme-level indicators only
- Local context review required
- Escalation path for sensitive data
- Separate analytics output from funding, eligibility, procurement, and policy decisions

## Example Workflow

1. Pipeline scores programme rows using reproducible public-development indicators.
2. Programme officer reviews rows above the capacity-support threshold.
3. Data governance reviewer checks source freshness, privacy maturity, and sensitive-context constraints.
4. Local implementation partner validates interpretation against country context.
5. M&E analyst records workshop, training, or follow-up actions.

## Dashboard Evidence In This Repo

- Grafana export: `grafana/capacity_support_dashboard.json`
- Monitoring line protocol: `artifacts/capacity_alerts_influx.lp`
- Batch run manifest: `artifacts/run_manifest.json`
- Feature mart SQL: `sql/feature_mart.duckdb.sql`
