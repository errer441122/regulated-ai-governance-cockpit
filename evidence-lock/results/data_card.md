# Data Card - Simulated Regulated Risk Dataset

## Dataset

`ml-baseline/data/simulated_regulated_risk_dataset.csv`

The dataset is generated deterministically by `ml-baseline/src/regulated_risk_ml/data.py` if it is missing.

## Purpose

The sample supports CRIF/PwC-style ML engineering review: feature engineering, train/test split, model comparison, calibration, drift/data-quality checks, and model-card generation.

## Schema Themes

- Company context: sector, region, company size, company age.
- Risk signals: sector risk, financial signal, late-payment signal, ESG/climate exposure, region macro risk, text risk, geographic distance risk.
- Data-quality signal: `data_quality_score`.
- Advisory flags: `human_review_required` and synthetic `target_default_or_escalation`.

## Data Classification

- Synthetic portfolio data.
- No real customer, company, credit, health, supplier, employee, or public-administration records.
- No credentials, secrets, or production exports.

## Quality Controls

- Required-column validation.
- Missing-value validation.
- Fixed random seed.
- Deterministic train/test split.
- Drift/data-quality report generated under `ml-baseline/artifacts/drift_report.json`.

## Restrictions

Do not describe this dataset as proprietary, production, customer-derived, CRIF-derived, PwC-derived, UNDP-derived, CINECA-derived, IT4LIA-derived, BI-REX-derived, or representative of a real regulated institution.
