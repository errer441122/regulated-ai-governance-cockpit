from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "public_development_sample.csv"


def load_indicator_rows(path: Path = DATA_PATH) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 8:
        raise ValueError("Expected at least 8 public-development sample rows.")
    return rows


def score_row(row: dict[str, Any]) -> dict[str, Any]:
    low_connectivity = max(0.0, 75.0 - float(row["internet_usage_pct"])) / 75.0
    unemployment = min(1.0, float(row["unemployment_pct"]) / 20.0)
    climate = min(1.0, float(row["climate_exposure_index"]) / 10.0)
    education_gap = max(0.0, 0.75 - float(row["education_index"])) / 0.75
    governance_gap = max(0.0, 0.65 - float(row["governance_signal"])) / 0.65
    score = 0.24 * low_connectivity + 0.18 * unemployment + 0.24 * climate + 0.16 * education_gap + 0.18 * governance_gap
    return {
        **row,
        "sdg_risk_score": round(score, 4),
        "capacity_support_flag": int(score >= 0.42),
    }


def build_features(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [score_row(row) for row in rows]
