from __future__ import annotations

import csv
import importlib.util
import json
import sqlite3
import sys
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = BASE_DIR / "artifacts"


def _load_pipeline_module():
    pipeline_path = BASE_DIR / "src" / "pipeline.py"
    spec = importlib.util.spec_from_file_location("production_capacity_pipeline", pipeline_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load production simulation pipeline.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


pipeline = _load_pipeline_module()


def write_predictions(scored: list[dict[str, object]], output_dir: Path) -> Path:
    path = output_dir / "capacity_support_predictions.csv"
    fields = [
        "programme_id",
        "country",
        "iso3",
        "region",
        "predicted_capacity_support_probability",
        "predicted_capacity_support",
        "needs_capacity_support",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in scored:
            writer.writerow({field: row[field] for field in fields})
    return path


def write_sqlite_mart(scored: list[dict[str, object]], output_dir: Path) -> Path:
    path = output_dir / "capacity_feature_mart.sqlite"
    if path.exists():
        path.unlink()
    with closing(sqlite3.connect(path)) as connection:
        connection.execute(
            """
            CREATE TABLE capacity_support_features (
                programme_id TEXT PRIMARY KEY,
                country TEXT NOT NULL,
                iso3 TEXT NOT NULL,
                region TEXT NOT NULL,
                internet_users_pct REAL NOT NULL,
                gov_effectiveness_score REAL NOT NULL,
                disaster_risk_index REAL NOT NULL,
                fragility_flag INTEGER NOT NULL,
                data_protection_maturity INTEGER NOT NULL,
                ai_readiness_score REAL NOT NULL,
                text_risk_hits INTEGER NOT NULL,
                predicted_capacity_support_probability REAL NOT NULL,
                needs_capacity_support INTEGER NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO capacity_support_features VALUES (
                :programme_id,
                :country,
                :iso3,
                :region,
                :internet_users_pct,
                :gov_effectiveness_score,
                :disaster_risk_index,
                :fragility_flag,
                :data_protection_maturity,
                :ai_readiness_score,
                :text_risk_hits,
                :predicted_capacity_support_probability,
                :needs_capacity_support
            )
            """,
            scored,
        )
        connection.commit()
    return path


def write_monitoring(scored: list[dict[str, object]], output_dir: Path) -> Path:
    path = output_dir / "capacity_alerts_influx.lp"
    lines = []
    for index, row in enumerate(scored):
        timestamp_ns = 1_735_689_600_000_000_000 + index * 60_000_000_000
        tags = f"iso3={row['iso3']},region={str(row['region']).replace(' ', '_')}"
        fields = (
            f"risk_probability={row['predicted_capacity_support_probability']},"
            f"text_risk_hits={row['text_risk_hits']}i,"
            f"fragility_flag={row['fragility_flag']}i"
        )
        lines.append(f"undp_capacity_support,{tags} {fields} {timestamp_ns}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_lifecycle_artifacts(metrics: dict[str, float], output_dir: Path) -> dict[str, Path]:
    run_id = datetime.now(timezone.utc).strftime("portfolio-%Y%m%d%H%M%S")
    mlflow_path = output_dir / "mlflow_run.json"
    mlflow_path.write_text(
        json.dumps(
            {
                "experiment": "portfolio-production-sim",
                "run_id": run_id,
                "tracking_uri": "http://localhost:5000",
                "params": {
                    "model_type": "transparent_weighted_baseline",
                    "threshold": pipeline.CAPACITY_SUPPORT_THRESHOLD,
                    "dataset": "world_bank_hdx_style_capacity_sample",
                },
                "metrics": metrics,
                "artifacts": [
                    "capacity_support_predictions.csv",
                    "capacity_feature_mart.sqlite",
                    "capacity_alerts_influx.lp",
                    "model_card.json",
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    minio_path = output_dir / "minio_manifest.json"
    minio_path.write_text(
        json.dumps(
            {
                "endpoint": "http://localhost:9000",
                "bucket": "portfolio-ml-artifacts",
                "objects": [
                    "s3://portfolio-ml-artifacts/capacity/model_card.json",
                    "s3://portfolio-ml-artifacts/capacity/predictions.csv",
                    "s3://portfolio-ml-artifacts/capacity/feature_mart.sqlite",
                ],
                "note": "Manifest only. Upload requires MinIO credentials and running docker-compose stack.",
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    model_card_path = output_dir / "model_card.json"
    model_card_path.write_text(
        json.dumps(
            {
                "model_name": "capacity_support_triage_baseline",
                "model_type": "transparent weighted baseline",
                "threshold": pipeline.CAPACITY_SUPPORT_THRESHOLD,
                "intended_use": "Human-reviewed prioritization for capacity-building support",
                "not_for": ["aid allocation automation", "eligibility decisions", "legal or policy decisions"],
                "metrics": metrics,
                "data_sources": [
                    "Offline World Bank/HDX-style sample for CI",
                    "World Bank API fetcher for network-enabled refresh",
                ],
                "limitations": [
                    "offline sample is small",
                    "no fairness certification",
                    "no live cloud deployment",
                    "no production security review",
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return {"mlflow": mlflow_path, "minio": minio_path, "model_card": model_card_path}


def run(output_dir: Path = ARTIFACT_DIR) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    scored = pipeline.score_records(pipeline.load_records())
    metrics = pipeline.evaluate(scored)
    predictions_path = write_predictions(scored, output_dir)
    mart_path = write_sqlite_mart(scored, output_dir)
    monitoring_path = write_monitoring(scored, output_dir)
    lifecycle = write_lifecycle_artifacts(metrics, output_dir)

    manifest_path = output_dir / "run_manifest.json"
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows": len(scored),
        "metrics": metrics,
        "artifacts": {
            "predictions": str(predictions_path),
            "mart": str(mart_path),
            "monitoring": str(monitoring_path),
            **{key: str(value) for key, value in lifecycle.items()},
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def main() -> None:
    manifest = run()
    metrics = manifest["metrics"]
    print(
        "Production simulation completed: "
        f"rows={manifest['rows']} "
        f"accuracy={metrics['accuracy']} "
        f"f1={metrics['f1']}"
    )


if __name__ == "__main__":
    main()
