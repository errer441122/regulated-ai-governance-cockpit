from __future__ import annotations

import csv
import json
import urllib.request
from pathlib import Path


BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=5"
COUNTRIES = ["KEN", "GHA", "NPL", "JOR", "COL", "RWA", "PER", "VNM"]
INDICATORS = {
    "internet_users_pct": "IT.NET.USER.ZS",
    "mobile_subscriptions_per_100": "IT.CEL.SETS.P2",
}


def fetch_indicator(country: str, indicator: str) -> float | None:
    url = BASE_URL.format(country=country, indicator=indicator)
    with urllib.request.urlopen(url, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    for item in payload[1] or []:
        if item.get("value") is not None:
            return float(item["value"])
    return None


def main() -> None:
    output_path = Path(__file__).resolve().parents[1] / "data" / "world_bank_refresh.csv"
    rows = []
    for country in COUNTRIES:
        row = {"iso3": country}
        for name, indicator in INDICATORS.items():
            row[name] = fetch_indicator(country, indicator)
        rows.append(row)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["iso3", *INDICATORS.keys()])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()
