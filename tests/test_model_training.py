from src.regulated_ai_governance.features import rule_probability


def test_rule_probability_is_bounded() -> None:
    probability = rule_probability(
        {
            "data_quality_score": 0.7,
            "governance_maturity": 0.6,
            "automation_complexity": 0.8,
            "stage_age_days": 30,
            "gdpr_sensitive": 1,
            "field_failure_signals": 0.2,
        }
    )
    assert 0.01 <= probability <= 0.99
