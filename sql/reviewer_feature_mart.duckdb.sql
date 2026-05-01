CREATE OR REPLACE TABLE stg_regulated_workflows AS
SELECT *
FROM read_csv_auto('hpc-mlops-industrial-lab/data/regulated_workflows.csv', HEADER = TRUE);

CREATE OR REPLACE VIEW mart_workflow_readiness AS
SELECT
  workflow_id,
  sector,
  region,
  data_quality_score,
  governance_maturity,
  automation_complexity,
  stage_age_days,
  gdpr_sensitive,
  field_failure_signals,
  needs_human_escalation,
  ROUND(
    data_quality_score * 0.35
    + governance_maturity * 12
    + (6 - automation_complexity) * 8
    - LEAST(stage_age_days, 120) * 0.12
    - field_failure_signals * 5,
    2
  ) AS readiness_index,
  CASE
    WHEN needs_human_escalation = 1 THEN 'human_review_required'
    WHEN data_quality_score >= 80 AND governance_maturity >= 4 THEN 'controlled_pilot_candidate'
    ELSE 'prepare_before_pilot'
  END AS reviewer_decision_band
FROM stg_regulated_workflows;

CREATE OR REPLACE VIEW dq_blocker_checks AS
SELECT
  workflow_id,
  sector,
  region,
  CASE WHEN data_quality_score < 70 THEN 1 ELSE 0 END AS low_data_quality,
  CASE WHEN governance_maturity < 3 THEN 1 ELSE 0 END AS weak_governance,
  CASE WHEN automation_complexity >= 5 THEN 1 ELSE 0 END AS high_automation_complexity,
  CASE WHEN field_failure_signals >= 2 THEN 1 ELSE 0 END AS industrial_signal_risk
FROM stg_regulated_workflows;

CREATE OR REPLACE VIEW reporting_sector_summary AS
SELECT
  sector,
  COUNT(*) AS workflow_count,
  ROUND(AVG(readiness_index), 2) AS avg_readiness_index,
  SUM(needs_human_escalation) AS human_review_queue,
  SUM(CASE WHEN reviewer_decision_band = 'controlled_pilot_candidate' THEN 1 ELSE 0 END) AS pilot_candidates
FROM mart_workflow_readiness
GROUP BY sector
ORDER BY avg_readiness_index DESC;
