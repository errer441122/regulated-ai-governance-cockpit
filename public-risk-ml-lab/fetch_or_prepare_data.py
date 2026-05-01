from __future__ import annotations

import csv
from pathlib import Path

from sklearn.datasets import load_breast_cancer


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "wisconsin_breast_cancer_public.csv"


def prepare_data(path: Path = DATA_PATH) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    dataset = load_breast_cancer()
    feature_names = [name.replace(" ", "_") for name in dataset.feature_names]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["record_id", *feature_names, "high_risk_label"])
        for index, (features, target) in enumerate(zip(dataset.data, dataset.target), start=1):
            high_risk_label = 1 if int(target) == 0 else 0
            writer.writerow([f"WDBC-{index:04d}", *[round(float(value), 6) for value in features], high_risk_label])
    return path


def main() -> None:
    path = prepare_data()
    print(f"Prepared public dataset: {path}")


if __name__ == "__main__":
    main()
