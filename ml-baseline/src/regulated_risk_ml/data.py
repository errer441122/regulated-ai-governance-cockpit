from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import DATA_PATH, REQUIRED_COLUMNS, TARGET_COLUMN


SECTORS = ["credit_risk", "insurance", "utilities", "public_sector", "manufacturing", "healthcare"]
REGIONS = ["Lombardy", "Emilia-Romagna", "Lazio", "Piedmont", "Campania", "Sicily"]
SIZE_BUCKETS = ["micro", "small", "mid_market", "enterprise"]


@dataclass
class RiskDatasetBuilder:
    """Build and validate a deterministic synthetic regulated-risk dataset."""

    path: Path = DATA_PATH
    rows: int = 360
    seed: int = 42

    def ensure_dataset(self) -> Path:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.write_dataset(self.generate_rows())
        return self.path

    def generate_rows(self) -> list[dict[str, Any]]:
        rng = random.Random(self.seed)
        records: list[dict[str, Any]] = []
        for index in range(self.rows):
            sector_index = index % len(SECTORS)
            region_index = (index * 2 + 1) % len(REGIONS)
            size_index = (index * 3 + 2) % len(SIZE_BUCKETS)
            sector_risk = 18 + sector_index * 9 + rng.randint(0, 18)
            data_quality = 94 - ((index * 7) % 55) - rng.randint(0, 8)
            financial_signal = 22 + ((index * 11) % 68) + rng.randint(-5, 5)
            esg_exposure = 8 + ((index * 5 + region_index * 4) % 75)
            late_payment = 4 + ((index * 13 + sector_index * 7) % 85)
            macro_risk = 12 + ((index * 3 + region_index * 11) % 78)
            text_risk = 6 + ((index * 17 + sector_index * 5) % 82)
            geo_risk = 4 + ((index * 19 + region_index * 3) % 76)
            company_age = 1 + ((index * 5 + rng.randint(0, 6)) % 35)

            raw_score = (
                0.18 * sector_risk
                + 0.16 * (100 - data_quality)
                + 0.16 * financial_signal
                + 0.10 * esg_exposure
                + 0.16 * late_payment
                + 0.10 * macro_risk
                + 0.09 * text_risk
                + 0.05 * geo_risk
                - 0.04 * min(company_age, 20)
            )
            human_review_required = int(raw_score >= 50 or data_quality < 55 or text_risk >= 72)
            target = int(raw_score >= 56 or (late_payment >= 75 and financial_signal >= 70))

            records.append(
                {
                    "record_id": f"RR-{index + 1:04d}",
                    "sector": SECTORS[sector_index],
                    "region": REGIONS[region_index],
                    "company_size_bucket": SIZE_BUCKETS[size_index],
                    "company_age_years": company_age,
                    "sector_risk_score": max(0, min(100, sector_risk)),
                    "data_quality_score": max(0, min(100, data_quality)),
                    "financial_signal_score": max(0, min(100, financial_signal)),
                    "esg_climate_exposure": max(0, min(100, esg_exposure)),
                    "late_payment_signal": max(0, min(100, late_payment)),
                    "region_macro_risk": max(0, min(100, macro_risk)),
                    "text_risk_score": max(0, min(100, text_risk)),
                    "geo_distance_risk": max(0, min(100, geo_risk)),
                    "human_review_required": human_review_required,
                    TARGET_COLUMN: target,
                }
            )
        return records

    def write_dataset(self, records: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=REQUIRED_COLUMNS)
            writer.writeheader()
            writer.writerows(records)

    def load_records(self) -> list[dict[str, Any]]:
        self.ensure_dataset()
        with self.path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return self.validate_records(rows)

    def validate_records(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if len(rows) < 300:
            raise ValueError("Risk ML baseline requires at least 300 synthetic rows.")
        missing = set(REQUIRED_COLUMNS) - set(rows[0])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        for row in rows:
            for column in REQUIRED_COLUMNS:
                if row.get(column) in (None, ""):
                    raise ValueError(f"Missing value in {column} for {row.get('record_id', 'unknown')}")
        return rows
