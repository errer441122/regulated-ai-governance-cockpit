#!/usr/bin/env bash
set -euo pipefail

python -m pip install -r requirements.txt
python -m pytest -q
python -m src.regulated_ai_governance.train
python public-risk-ml-lab/fetch_or_prepare_data.py
python public-risk-ml-lab/train.py
python public-risk-ml-lab/evaluate.py
python business-data-quality-lab/validate_registry_like_records.py
python business-data-quality-lab/duplicate_detection.py
python undp-public-data-gis-lab/sdg_indicator_analysis.py
python hpc-pytorch-benchmark/benchmark.py --quick
python -m src.regulated_ai_governance.evaluate
python -m src.regulated_ai_governance.api_smoke_test
python scripts/build_evidence_report.py
