from src.regulated_ai_governance.data_validation import validate_dataset


def test_regulated_dataset_contract_passes() -> None:
    report = validate_dataset()
    assert report["status"] == "passed"
    assert report["rows"] > 20
