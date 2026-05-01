from pathlib import Path
import sys


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from regulated_risk_ml.features import FeatureEngineer, rule_baseline


def test_feature_engineer_casts_numeric_and_keeps_categories():
    row = {
        "sector": "credit_risk",
        "region": "Lombardy",
        "company_size_bucket": "mid_market",
        "company_age_years": "8",
        "sector_risk_score": "72",
        "data_quality_score": "52",
        "financial_signal_score": "81",
        "esg_climate_exposure": "35",
        "late_payment_signal": "77",
        "region_macro_risk": "55",
        "text_risk_score": "74",
        "geo_distance_risk": "42",
    }
    features = FeatureEngineer().transform_record(row)

    assert features["sector"] == "credit_risk"
    assert features["data_quality_score"] == 52.0
    assert rule_baseline(row) == 1
