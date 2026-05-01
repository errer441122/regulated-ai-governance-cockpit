from src.regulated_ai_governance.api import smoke_test


def test_api_smoke_contract() -> None:
    payload = smoke_test()
    assert payload["health"]["status"] == "ok"
    assert "predicted_review_escalation_probability" in payload["score"]
