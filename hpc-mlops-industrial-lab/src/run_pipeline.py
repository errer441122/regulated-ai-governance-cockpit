from __future__ import annotations

import csv
import json
import math
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "regulated_workflows.csv"
ARTIFACT_DIR = BASE_DIR / "artifacts"
BOLOGNA_LAT = 44.4949
BOLOGNA_LON = 11.3426

REQUIRED_COLUMNS = {
    "workflow_id",
    "sector",
    "region",
    "lat",
    "lon",
    "data_quality_score",
    "governance_maturity",
    "automation_complexity",
    "stage_age_days",
    "gdpr_sensitive",
    "field_failure_signals",
    "case_notes",
    "needs_human_escalation",
}

RISK_TERMS = {
    "missing",
    "complaint",
    "manual",
    "override",
    "dispute",
    "anomaly",
    "incomplete",
    "sensitive",
    "exception",
    "stale",
    "drift",
}

FEATURE_NAMES = [
    "data_quality_score",
    "governance_maturity",
    "automation_complexity",
    "stage_age_days",
    "gdpr_sensitive",
    "field_failure_signals",
    "text_risk_hits",
    "distance_to_bologna_km",
]

INDUSTRIAL_MESSAGE_REQUIRED = {
    "topic",
    "asset_id",
    "timestamp_utc",
    "temperature_c",
    "vibration_mm_s",
    "cycle_time_ms",
    "quality_flag",
}


@dataclass
class ModelBundle:
    feature_names: list[str]
    weights: list[float]
    means: list[float]
    scales: list[float]
    threshold: float = 0.5


def _to_float(value: str, column: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"Column {column} must be numeric, got {value!r}") from exc


def _to_int(value: str, column: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Column {column} must be an integer, got {value!r}") from exc


def load_rows(path: Path = DATA_PATH) -> list[dict[str, object]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        rows: list[dict[str, object]] = []
        for raw in reader:
            rows.append(
                {
                    "workflow_id": raw["workflow_id"],
                    "sector": raw["sector"],
                    "region": raw["region"],
                    "lat": _to_float(raw["lat"], "lat"),
                    "lon": _to_float(raw["lon"], "lon"),
                    "data_quality_score": _to_float(raw["data_quality_score"], "data_quality_score"),
                    "governance_maturity": _to_int(raw["governance_maturity"], "governance_maturity"),
                    "automation_complexity": _to_int(raw["automation_complexity"], "automation_complexity"),
                    "stage_age_days": _to_int(raw["stage_age_days"], "stage_age_days"),
                    "gdpr_sensitive": _to_int(raw["gdpr_sensitive"], "gdpr_sensitive"),
                    "field_failure_signals": _to_int(raw["field_failure_signals"], "field_failure_signals"),
                    "case_notes": raw["case_notes"],
                    "needs_human_escalation": _to_int(raw["needs_human_escalation"], "needs_human_escalation"),
                }
            )

    if len(rows) < 20:
        raise ValueError("The lab needs at least 20 rows to make train/test metrics meaningful.")
    return rows


def haversine_km(lat_a: float, lon_a: float, lat_b: float, lon_b: float) -> float:
    radius_km = 6371.0
    phi_a = math.radians(lat_a)
    phi_b = math.radians(lat_b)
    delta_phi = math.radians(lat_b - lat_a)
    delta_lambda = math.radians(lon_b - lon_a)

    step = math.sin(delta_phi / 2) ** 2
    step += math.cos(phi_a) * math.cos(phi_b) * math.sin(delta_lambda / 2) ** 2
    return 2 * radius_km * math.atan2(math.sqrt(step), math.sqrt(1 - step))


def count_text_risk_hits(text: str) -> int:
    tokens = {token.strip(".,:;()[]").lower() for token in text.split()}
    return len(tokens & RISK_TERMS)


def validate_industrial_message(payload: dict[str, object]) -> dict[str, object]:
    missing = sorted(INDUSTRIAL_MESSAGE_REQUIRED - set(payload))
    topic = str(payload.get("topic", ""))
    asset_id = str(payload.get("asset_id", ""))
    numeric_fields = ["temperature_c", "vibration_mm_s", "cycle_time_ms"]
    numeric_errors = []
    for field in numeric_fields:
        try:
            float(payload.get(field, ""))
        except (TypeError, ValueError):
            numeric_errors.append(field)

    topic_matches_asset = bool(topic.startswith("factory/") and asset_id and asset_id in topic)
    valid = not missing and not numeric_errors and topic_matches_asset
    return {
        "valid": valid,
        "asset_id": asset_id,
        "protocol_style": "mqtt-opcua-telemetry",
        "missing_fields": missing,
        "numeric_errors": numeric_errors,
        "topic_matches_asset": topic_matches_asset,
    }


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, value))


def industrial_anomaly_score(payload: dict[str, object]) -> float:
    temperature = float(payload.get("temperature_c", 0.0))
    vibration = float(payload.get("vibration_mm_s", 0.0))
    cycle_time = float(payload.get("cycle_time_ms", 0.0))
    quality_flag = str(payload.get("quality_flag", "ok")).lower()

    quality_score = {"ok": 0.0, "warning": 0.6, "critical": 1.0}.get(quality_flag, 0.4)
    score = (
        0.30 * _bounded((temperature - 65.0) / 25.0)
        + 0.35 * _bounded((vibration - 3.0) / 5.0)
        + 0.20 * _bounded((cycle_time - 1000.0) / 600.0)
        + 0.15 * quality_score
    )
    return round(_bounded(score), 4)


def threshold_operating_summary(scores: list[float], threshold: float = 0.5) -> dict[str, float]:
    alerts = sum(1 for score in scores if score >= threshold)
    sorted_scores = sorted(scores)
    p95_index = min(len(sorted_scores) - 1, int(math.ceil(0.95 * len(sorted_scores))) - 1) if sorted_scores else 0
    return {
        "threshold": threshold,
        "records": len(scores),
        "alerts": alerts,
        "alert_rate": round(alerts / len(scores), 4) if scores else 0.0,
        "max_score": round(max(scores), 4) if scores else 0.0,
        "p95_score": round(sorted_scores[p95_index], 4) if sorted_scores else 0.0,
    }


def enrich_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    enriched: list[dict[str, object]] = []
    for row in rows:
        next_row = dict(row)
        next_row["text_risk_hits"] = count_text_risk_hits(str(row["case_notes"]))
        next_row["distance_to_bologna_km"] = round(
            haversine_km(float(row["lat"]), float(row["lon"]), BOLOGNA_LAT, BOLOGNA_LON),
            2,
        )
        enriched.append(next_row)
    return enriched


def build_matrix(rows: list[dict[str, object]]) -> tuple[list[list[float]], list[int]]:
    features = [[float(row[name]) for name in FEATURE_NAMES] for row in rows]
    labels = [int(row["needs_human_escalation"]) for row in rows]
    return features, labels


def split_train_test(features: list[list[float]], labels: list[int]) -> tuple[list[list[float]], list[int], list[list[float]], list[int]]:
    train_x: list[list[float]] = []
    train_y: list[int] = []
    test_x: list[list[float]] = []
    test_y: list[int] = []

    for index, (feature_row, label) in enumerate(zip(features, labels)):
        if index % 4 == 0:
            test_x.append(feature_row)
            test_y.append(label)
        else:
            train_x.append(feature_row)
            train_y.append(label)

    return train_x, train_y, test_x, test_y


def fit_standardizer(features: list[list[float]]) -> tuple[list[float], list[float]]:
    columns = list(zip(*features))
    means = [mean(column) for column in columns]
    scales = [pstdev(column) or 1.0 for column in columns]
    return means, scales


def transform(features: list[list[float]], means: list[float], scales: list[float]) -> list[list[float]]:
    return [
        [(value - means[index]) / scales[index] for index, value in enumerate(row)]
        for row in features
    ]


def sigmoid(value: float) -> float:
    if value < -35:
        return 0.0
    if value > 35:
        return 1.0
    return 1.0 / (1.0 + math.exp(-value))


def train_logistic_regression(
    features: list[list[float]],
    labels: list[int],
    epochs: int = 1800,
    learning_rate: float = 0.08,
    l2_penalty: float = 0.001,
) -> list[float]:
    weights = [0.0 for _ in range(len(features[0]) + 1)]
    sample_count = len(labels)

    for _ in range(epochs):
        gradients = [0.0 for _ in weights]
        for row, label in zip(features, labels):
            score = weights[0] + sum(weight * value for weight, value in zip(weights[1:], row))
            error = sigmoid(score) - label
            gradients[0] += error
            for index, value in enumerate(row, start=1):
                gradients[index] += error * value

        for index in range(len(weights)):
            regularization = 0.0 if index == 0 else l2_penalty * weights[index]
            weights[index] -= learning_rate * ((gradients[index] / sample_count) + regularization)

    return weights


def predict_probabilities(features: list[list[float]], weights: list[float]) -> list[float]:
    probabilities: list[float] = []
    for row in features:
        score = weights[0] + sum(weight * value for weight, value in zip(weights[1:], row))
        probabilities.append(sigmoid(score))
    return probabilities


def evaluate(labels: list[int], probabilities: list[float], threshold: float = 0.5) -> dict[str, float]:
    predictions = [1 if probability >= threshold else 0 for probability in probabilities]
    tp = sum(1 for expected, actual in zip(labels, predictions) if expected == 1 and actual == 1)
    tn = sum(1 for expected, actual in zip(labels, predictions) if expected == 0 and actual == 0)
    fp = sum(1 for expected, actual in zip(labels, predictions) if expected == 0 and actual == 1)
    fn = sum(1 for expected, actual in zip(labels, predictions) if expected == 1 and actual == 0)

    accuracy = (tp + tn) / len(labels)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
    }


def write_sqlite_mart(rows: list[dict[str, object]], probabilities: list[float], output_dir: Path) -> Path:
    mart_path = output_dir / "regulated_feature_mart.sqlite"
    if mart_path.exists():
        mart_path.unlink()

    with closing(sqlite3.connect(mart_path)) as connection:
        connection.execute(
            """
            CREATE TABLE regulated_workflow_features (
                workflow_id TEXT PRIMARY KEY,
                sector TEXT NOT NULL,
                region TEXT NOT NULL,
                data_quality_score REAL NOT NULL,
                governance_maturity INTEGER NOT NULL,
                automation_complexity INTEGER NOT NULL,
                stage_age_days INTEGER NOT NULL,
                gdpr_sensitive INTEGER NOT NULL,
                field_failure_signals INTEGER NOT NULL,
                text_risk_hits INTEGER NOT NULL,
                distance_to_bologna_km REAL NOT NULL,
                predicted_escalation_probability REAL NOT NULL,
                needs_human_escalation INTEGER NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO regulated_workflow_features VALUES (
                :workflow_id,
                :sector,
                :region,
                :data_quality_score,
                :governance_maturity,
                :automation_complexity,
                :stage_age_days,
                :gdpr_sensitive,
                :field_failure_signals,
                :text_risk_hits,
                :distance_to_bologna_km,
                :predicted_escalation_probability,
                :needs_human_escalation
            )
            """,
            [
                {
                    **row,
                    "predicted_escalation_probability": round(probability, 4),
                }
                for row, probability in zip(rows, probabilities)
            ],
        )
        connection.commit()
    return mart_path


def write_artifacts(
    rows: list[dict[str, object]],
    all_probabilities: list[float],
    metrics: dict[str, float],
    bundle: ModelBundle,
    output_dir: Path,
) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    predictions_path = output_dir / "escalation_predictions.csv"
    with predictions_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "workflow_id",
            "sector",
            "region",
            "predicted_escalation_probability",
            "predicted_human_escalation",
            "needs_human_escalation",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row, probability in zip(rows, all_probabilities):
            writer.writerow(
                {
                    "workflow_id": row["workflow_id"],
                    "sector": row["sector"],
                    "region": row["region"],
                    "predicted_escalation_probability": round(probability, 4),
                    "predicted_human_escalation": int(probability >= bundle.threshold),
                    "needs_human_escalation": row["needs_human_escalation"],
                }
            )

    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")

    model_card_path = output_dir / "model_card.json"
    model_card = {
        "model_name": "regulated_workflow_human_escalation_classifier",
        "model_type": "logistic_regression_from_scratch",
        "target": "needs_human_escalation",
        "decision_boundary": "advisory triage only; no automated rejection or approval",
        "feature_names": bundle.feature_names,
        "metrics": metrics,
        "limitations": [
            "simulated data only",
            "small sample size",
            "not calibrated for production",
            "no fairness certification",
            "no live cloud or HPC execution",
        ],
    }
    model_card_path.write_text(json.dumps(model_card, indent=2, sort_keys=True), encoding="utf-8")

    industrial_scores = [
        industrial_anomaly_score(
            {
                "temperature_c": 50.0 + float(row["field_failure_signals"]) * 9.0,
                "vibration_mm_s": 1.5 + float(row["field_failure_signals"]) * 1.4,
                "cycle_time_ms": 850 + int(row["stage_age_days"]) * 8,
                "quality_flag": "warning" if int(row["field_failure_signals"]) >= 3 else "ok",
            }
        )
        for row in rows
    ]
    industrial_monitoring_path = output_dir / "industrial_monitoring_summary.json"
    industrial_monitoring_path.write_text(
        json.dumps(
            {
                "schema": "mqtt-opcua-telemetry",
                "anomaly_threshold": 0.5,
                "threshold_summary": threshold_operating_summary(industrial_scores, threshold=0.5),
                "boundary": "simulated telemetry-style evidence only; not connected to factory systems",
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    manifest_path = output_dir / "run_manifest.json"
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows": len(rows),
        "artifacts": [
            str(predictions_path.name),
            str(metrics_path.name),
            str(model_card_path.name),
            str(industrial_monitoring_path.name),
            "regulated_feature_mart.sqlite",
        ],
        "review_boundary": "human reviewer must approve any escalation action",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    return {
        "predictions": str(predictions_path),
        "metrics": str(metrics_path),
        "model_card": str(model_card_path),
        "industrial_monitoring": str(industrial_monitoring_path),
        "manifest": str(manifest_path),
    }


def run_pipeline(output_dir: Path = ARTIFACT_DIR) -> dict[str, object]:
    rows = enrich_rows(load_rows())
    features, labels = build_matrix(rows)
    train_x, train_y, test_x, test_y = split_train_test(features, labels)

    means, scales = fit_standardizer(train_x)
    train_x_scaled = transform(train_x, means, scales)
    test_x_scaled = transform(test_x, means, scales)
    all_x_scaled = transform(features, means, scales)

    weights = train_logistic_regression(train_x_scaled, train_y)
    test_probabilities = predict_probabilities(test_x_scaled, weights)
    all_probabilities = predict_probabilities(all_x_scaled, weights)
    metrics = evaluate(test_y, test_probabilities)

    bundle = ModelBundle(
        feature_names=FEATURE_NAMES,
        weights=[round(weight, 6) for weight in weights],
        means=[round(value, 6) for value in means],
        scales=[round(value, 6) for value in scales],
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    mart_path = write_sqlite_mart(rows, all_probabilities, output_dir)
    artifacts = write_artifacts(rows, all_probabilities, metrics, bundle, output_dir)

    return {
        "rows": len(rows),
        "metrics": metrics,
        "model": bundle,
        "mart": str(mart_path),
        "artifacts": artifacts,
    }


def main() -> None:
    result = run_pipeline()
    metrics = result["metrics"]
    print(
        "HPC/MLOps lab completed: "
        f"rows={result['rows']} "
        f"accuracy={metrics['accuracy']} "
        f"f1={metrics['f1']}"
    )


if __name__ == "__main__":
    main()
