.PHONY: setup test test-node test-python train evaluate smoke docs public-risk data-quality undp-gis hpc-pytorch evidence

setup:
	python -m pip install -r requirements.txt

test: test-node test-python

test-node:
	npm test

test-python:
	python -m pytest -q

train:
	python -m src.regulated_ai_governance.train

evaluate: public-risk data-quality undp-gis hpc-pytorch
	python -m src.regulated_ai_governance.evaluate

smoke:
	python -m src.regulated_ai_governance.api_smoke_test

docs:
	python scripts/build_reviewer_summary.py

public-risk:
	python public-risk-ml-lab/fetch_or_prepare_data.py
	python public-risk-ml-lab/train.py
	python public-risk-ml-lab/evaluate.py

data-quality:
	python business-data-quality-lab/validate_registry_like_records.py
	python business-data-quality-lab/duplicate_detection.py

undp-gis:
	python undp-public-data-gis-lab/sdg_indicator_analysis.py

hpc-pytorch:
	python hpc-pytorch-benchmark/benchmark.py --quick

evidence: test train evaluate smoke
	python scripts/build_evidence_report.py
