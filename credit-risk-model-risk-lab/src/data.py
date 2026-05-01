from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import arff
from sklearn.model_selection import train_test_split

from fetch_data import RAW_DATA_PATH, fetch


FEATURE_COLUMNS = [
    "RevolvingUtilizationOfUnsecuredLines",
    "age",
    "NumberOfTime30-59DaysPastDueNotWorse",
    "DebtRatio",
    "MonthlyIncome",
    "NumberOfOpenCreditLinesAndLoans",
    "NumberOfTimes90DaysLate",
    "NumberRealEstateLoansOrLines",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberOfDependents",
]
TARGET_COLUMN = "FinancialDistressNextTwoYears"


def ensure_data(path: Path = RAW_DATA_PATH) -> Path:
    if not path.exists():
        fetch()
    return path


def load_dataset(path: Path = RAW_DATA_PATH) -> tuple[np.ndarray, np.ndarray]:
    ensure_data(path)
    records, _ = arff.loadarff(path)
    features = np.column_stack([records[column].astype(float) for column in FEATURE_COLUMNS])
    raw_target = records[TARGET_COLUMN]
    target = np.array([1 if value in {b"Yes", "Yes", 1} else 0 for value in raw_target], dtype=int)
    return features, target


def split_dataset(random_state: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    features, target = load_dataset()
    return train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=random_state,
        stratify=target,
    )
