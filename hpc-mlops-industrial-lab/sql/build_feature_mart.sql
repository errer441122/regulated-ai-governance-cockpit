-- Reviewer-facing SQL sketch for the feature mart built by src/run_pipeline.py.
-- The executable pipeline uses sqlite3 directly so the lab has no external dependency.

CREATE TABLE IF NOT EXISTS regulated_workflow_features (
    workflow_id TEXT PRIMARY KEY,
    sector TEXT NOT NULL,
    region TEXT NOT NULL,
    data_quality_score REAL NOT NULL,
    governance_maturity INTEGER NOT NULL,
    automation_complexity INTEGER NOT NULL,
    stage_age_days INTEGER NOT NULL,
    gdpr_sensitive INTEGER NOT NULL,
    field_failure_signals INTEGER NOT NULL,
    text_risk_hits INTEGER NOT NULL,
    distance_to_bologna_km REAL NOT NULL,
    predicted_escalation_probability REAL NOT NULL,
    needs_human_escalation INTEGER NOT NULL
);
