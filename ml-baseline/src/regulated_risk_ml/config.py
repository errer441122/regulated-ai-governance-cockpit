from __future__ import annotations

from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = PACKAGE_DIR.parent
DATA_DIR = PACKAGE_DIR / "data"
ARTIFACT_DIR = PACKAGE_DIR / "artifacts"
REPORT_DIR = PACKAGE_DIR / "reports"
DATA_PATH = DATA_DIR / "simulated_regulated_risk_dataset.csv"
MODEL_ARTIFACT_PATH = ARTIFACT_DIR / "model.joblib"

RANDOM_SEED = 42
TARGET_COLUMN = "target_default_or_escalation"

REQUIRED_COLUMNS = [
    "record_id",
    "sector",
    "region",
    "company_size_bucket",
    "company_age_years",
    "sector_risk_score",
    "data_quality_score",
    "financial_signal_score",
    "esg_climate_exposure",
    "late_payment_signal",
    "region_macro_risk",
    "text_risk_score",
    "geo_distance_risk",
    "human_review_required",
    "target_default_or_escalation",
]

NUMERIC_FEATURES = [
    "company_age_years",
    "sector_risk_score",
    "data_quality_score",
    "financial_signal_score",
    "esg_climate_exposure",
    "late_payment_signal",
    "region_macro_risk",
    "text_risk_score",
    "geo_distance_risk",
]

CATEGORICAL_FEATURES = ["sector", "region", "company_size_bucket"]
MODEL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

CALIBRATION_BINS = 10
