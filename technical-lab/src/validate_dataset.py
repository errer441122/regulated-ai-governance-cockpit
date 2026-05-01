from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "workflow_signals.csv"
REPORTS_DIR = ROOT / "reports"

REQUIRED_COLUMNS = {
    "organization",
    "sector",
    "use_case",
    "data_source",
    "data_sensitivity",
    "metadata_quality",
    "process_maturity",
    "stakeholder_clarity",
    "automation_potential",
    "ai_governance_readiness",
    "estimated_users",
    "criticality",
    "approved_for_brief",
}

SCORE_COLUMNS = [
    "metadata_quality",
    "process_maturity",
    "stakeholder_clarity",
    "automation_potential",
    "ai_governance_readiness",
]


def load_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def readiness_score(row: pd.Series) -> float:
    weights = {
        "metadata_quality": 0.25,
        "process_maturity": 0.15,
        "stakeholder_clarity": 0.20,
        "automation_potential": 0.15,
        "ai_governance_readiness": 0.25,
    }
    return round(sum(float(row[column]) * weight for column, weight in weights.items()), 2)


def classify_readiness(score: float) -> str:
    if score >= 4.2:
        return "ready_for_controlled_pilot"
    if score >= 3.4:
        return "needs_targeted_preparation"
    return "needs_foundation_work"


def validate(df: pd.DataFrame) -> dict:
    issues: list[str] = []

    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    unexpected_columns = sorted(set(df.columns) - REQUIRED_COLUMNS)
    if missing_columns:
        issues.append(f"Missing required columns: {', '.join(missing_columns)}")

    duplicate_count = int(df.duplicated(subset=["organization", "use_case"]).sum())
    if duplicate_count:
        issues.append(f"Duplicate organization/use_case rows: {duplicate_count}")

    missing_values = df[list(REQUIRED_COLUMNS & set(df.columns))].isna().sum()
    missing_value_issues = {column: int(count) for column, count in missing_values.items() if count}
    if missing_value_issues:
        issues.append(f"Missing values detected: {missing_value_issues}")

    for column in SCORE_COLUMNS:
        if column in df.columns:
            invalid = df[~df[column].between(1, 5)]
            if not invalid.empty:
                issues.append(f"{column} has values outside 1-5 scale: {len(invalid)} rows")

    if "approved_for_brief" in df.columns:
        allowed = {"yes", "no"}
        invalid_approval = sorted(set(df["approved_for_brief"].str.lower()) - allowed)
        if invalid_approval:
            issues.append(f"approved_for_brief has invalid labels: {invalid_approval}")

    scored = df.copy()
    scored["readiness_score"] = scored.apply(readiness_score, axis=1)
    scored["readiness_class"] = scored["readiness_score"].apply(classify_readiness)

    report = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_count": duplicate_count,
        "issues": issues,
        "ready_for_brief_count": int((df["approved_for_brief"].str.lower() == "yes").sum()),
        "average_readiness_score": round(float(scored["readiness_score"].mean()), 2),
        "readiness_class_counts": scored["readiness_class"].value_counts().to_dict(),
    }

    return {"report": report, "scored": scored}


def main() -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    df = load_dataset()
    result = validate(df)

    (REPORTS_DIR / "validation_report.json").write_text(
        json.dumps(result["report"], indent=2),
        encoding="utf-8",
    )
    result["scored"].to_csv(REPORTS_DIR / "readiness_scores.csv", index=False)

    if result["report"]["issues"]:
        print("Dataset validation completed with issues.")
        for issue in result["report"]["issues"]:
            print(f"- {issue}")
        raise SystemExit(1)

    print("Dataset validation passed.")
    print(f"Average readiness score: {result['report']['average_readiness_score']}")


if __name__ == "__main__":
    main()
