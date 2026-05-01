from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "public_development_sample.csv"

RISK_TERMS = {
    "capacity",
    "connectivity",
    "crisis",
    "cyber",
    "displacement",
    "drought",
    "earthquake",
    "flood",
    "fragile",
    "gap",
    "privacy",
    "protection",
    "procurement",
    "risk",
}

CAPACITY_SUPPORT_THRESHOLD = 0.3


def _float(value: str, column: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"{column} must be numeric, got {value!r}") from exc


def _int(value: str, column: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{column} must be an integer, got {value!r}") from exc


def load_records(path: Path = DATA_PATH) -> list[dict[str, object]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = []
        for raw in csv.DictReader(handle):
            rows.append(
                {
                    "programme_id": raw["programme_id"],
                    "country": raw["country"],
                    "iso3": raw["iso3"],
                    "year": _int(raw["year"], "year"),
                    "region": raw["region"],
                    "internet_users_pct": _float(raw["internet_users_pct"], "internet_users_pct"),
                    "mobile_subscriptions_per_100": _float(raw["mobile_subscriptions_per_100"], "mobile_subscriptions_per_100"),
                    "gov_effectiveness_score": _float(raw["gov_effectiveness_score"], "gov_effectiveness_score"),
                    "disaster_risk_index": _float(raw["disaster_risk_index"], "disaster_risk_index"),
                    "fragility_flag": _int(raw["fragility_flag"], "fragility_flag"),
                    "data_protection_maturity": _int(raw["data_protection_maturity"], "data_protection_maturity"),
                    "ai_readiness_score": _float(raw["ai_readiness_score"], "ai_readiness_score"),
                    "case_notes": raw["case_notes"],
                    "needs_capacity_support": _int(raw["needs_capacity_support"], "needs_capacity_support"),
                }
            )
    if len(rows) < 15:
        raise ValueError("Expected at least 15 public-development sample rows.")
    return rows


def count_text_risk_hits(text: str) -> int:
    tokens = {token.strip(".,:;()[]").lower() for token in text.split()}
    return len(tokens & RISK_TERMS)


def score_record(record: dict[str, object]) -> float:
    low_connectivity = max(0.0, 75.0 - float(record["internet_users_pct"])) / 75.0
    weak_governance = max(0.0, 0.5 - float(record["gov_effectiveness_score"])) / 2.5
    disaster = float(record["disaster_risk_index"]) / 10.0
    fragility = float(record["fragility_flag"])
    weak_data_protection = max(0.0, 5.0 - float(record["data_protection_maturity"])) / 5.0
    low_ai_readiness = max(0.0, 75.0 - float(record["ai_readiness_score"])) / 75.0
    text_risk = min(1.0, count_text_risk_hits(str(record["case_notes"])) / 4.0)

    probability = (
        0.18 * low_connectivity
        + 0.15 * weak_governance
        + 0.17 * disaster
        + 0.18 * fragility
        + 0.14 * weak_data_protection
        + 0.10 * low_ai_readiness
        + 0.08 * text_risk
    )
    return round(min(max(probability, 0.0), 1.0), 4)


def score_records(records: list[dict[str, object]]) -> list[dict[str, object]]:
    scored = []
    for record in records:
        probability = score_record(record)
        scored.append(
            {
                **record,
                "text_risk_hits": count_text_risk_hits(str(record["case_notes"])),
                "predicted_capacity_support_probability": probability,
                "predicted_capacity_support": int(probability >= CAPACITY_SUPPORT_THRESHOLD),
            }
        )
    return scored


def evaluate(scored: list[dict[str, object]]) -> dict[str, float]:
    labels = [int(row["needs_capacity_support"]) for row in scored]
    predictions = [int(row["predicted_capacity_support"]) for row in scored]
    tp = sum(1 for expected, actual in zip(labels, predictions) if expected == 1 and actual == 1)
    tn = sum(1 for expected, actual in zip(labels, predictions) if expected == 0 and actual == 0)
    fp = sum(1 for expected, actual in zip(labels, predictions) if expected == 0 and actual == 1)
    fn = sum(1 for expected, actual in zip(labels, predictions) if expected == 1 and actual == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "accuracy": round((tp + tn) / len(labels), 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
    }


def to_jsonable(scored: list[dict[str, object]]) -> list[dict[str, object]]:
    return [json.loads(json.dumps(row)) for row in scored]
