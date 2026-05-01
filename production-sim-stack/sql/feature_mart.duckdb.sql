-- DuckDB/dbt-style feature mart sketch for the production simulation stack.
-- Run from the production-sim-stack directory when DuckDB is installed:
-- duckdb artifacts/capacity_feature_mart.duckdb < sql/feature_mart.duckdb.sql

CREATE OR REPLACE TABLE raw_public_development AS
SELECT *
FROM read_csv_auto('data/public_development_sample.csv', HEADER = TRUE);

CREATE OR REPLACE TABLE capacity_support_feature_mart AS
SELECT
    programme_id,
    country,
    iso3,
    region,
    year,
    internet_users_pct,
    mobile_subscriptions_per_100,
    gov_effectiveness_score,
    disaster_risk_index,
    fragility_flag,
    data_protection_maturity,
    ai_readiness_score,
    CASE WHEN internet_users_pct < 50 THEN 1 ELSE 0 END AS low_connectivity_flag,
    CASE WHEN disaster_risk_index >= 7 THEN 1 ELSE 0 END AS high_disaster_risk_flag,
    CASE WHEN data_protection_maturity <= 2 THEN 1 ELSE 0 END AS weak_data_protection_flag,
    needs_capacity_support
FROM raw_public_development;
