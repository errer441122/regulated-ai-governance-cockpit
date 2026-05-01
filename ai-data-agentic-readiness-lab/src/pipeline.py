from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "workflow_candidates.csv"
REPORTS_DIR = ROOT / "reports"

REQUIRED_COLUMNS = {
    "workflow_id",
    "organization",
    "sector",
    "use_case",
    "data_source",
    "data_sensitivity",
    "metadata_quality",
    "data_governance",
    "stakeholder_clarity",
    "data_engineering_maturity",
    "reporting_value",
    "ai_workload_fit",
    "estimated_users",
    "owner_named",
    "agentic_use_approved",
    "domain",
}

SCORE_WEIGHTS = {
    "metadata_quality": 0.20,
    "data_governance": 0.20,
    "stakeholder_clarity": 0.15,
    "data_engineering_maturity": 0.15,
    "reporting_value": 0.15,
    "ai_workload_fit": 0.15,
}


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def validate_schema(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        issues.append(f"Missing columns: {', '.join(missing_columns)}")

    duplicate_ids = int(df["workflow_id"].duplicated().sum()) if "workflow_id" in df.columns else 0
    if duplicate_ids:
        issues.append(f"Duplicate workflow_id rows: {duplicate_ids}")

    for column in SCORE_WEIGHTS:
        if column in df.columns:
            invalid_count = int((~df[column].between(1, 5)).sum())
            if invalid_count:
                issues.append(f"{column} has {invalid_count} values outside 1-5")

    for column in ["owner_named", "agentic_use_approved"]:
        if column in df.columns:
            invalid = sorted(set(df[column].str.lower()) - {"yes", "no"})
            if invalid:
                issues.append(f"{column} has invalid values: {invalid}")

    return issues


def readiness_score(row: pd.Series) -> float:
    score = sum(float(row[column]) * weight for column, weight in SCORE_WEIGHTS.items())
    return round(score, 2)


def readiness_class(score: float) -> str:
    if score >= 4.25:
        return "controlled_pilot_ready"
    if score >= 3.5:
        return "prepare_then_pilot"
    if score >= 2.75:
        return "foundation_work_needed"
    return "not_ready"


def detect_blockers(row: pd.Series) -> list[str]:
    blockers: list[str] = []
    sensitivity = str(row["data_sensitivity"]).lower()

    if sensitivity == "high" and int(row["data_governance"]) < 4:
        blockers.append("high_sensitivity_weak_governance")
    if int(row["metadata_quality"]) < 3:
        blockers.append("metadata_quality_below_threshold")
    if str(row["owner_named"]).lower() != "yes":
        blockers.append("owner_not_named")
    if str(row["agentic_use_approved"]).lower() != "yes":
        blockers.append("agentic_use_not_approved")
    if int(row["stakeholder_clarity"]) < 3:
        blockers.append("stakeholder_clarity_below_threshold")

    return blockers


def score_dataset(df: pd.DataFrame) -> pd.DataFrame:
    scored = df.copy()
    scored["readiness_score"] = scored.apply(readiness_score, axis=1)
    scored["readiness_class"] = scored["readiness_score"].apply(readiness_class)
    scored["blockers"] = scored.apply(lambda row: ";".join(detect_blockers(row)), axis=1)
    scored["has_blockers"] = scored["blockers"].str.len() > 0
    return scored


def build_summary(scored: pd.DataFrame, schema_issues: list[str]) -> dict:
    return {
        "row_count": int(len(scored)),
        "schema_issues": schema_issues,
        "average_readiness_score": round(float(scored["readiness_score"].mean()), 2),
        "controlled_pilot_ready_count": int((scored["readiness_class"] == "controlled_pilot_ready").sum()),
        "blocked_count": int(scored["has_blockers"].sum()),
        "top_domains": scored["domain"].value_counts().head(5).to_dict(),
        "readiness_classes": scored["readiness_class"].value_counts().to_dict(),
        "top_candidates": scored.sort_values("readiness_score", ascending=False)[
            ["workflow_id", "organization", "use_case", "readiness_score", "readiness_class"]
        ].head(5).to_dict(orient="records"),
    }


def write_reports(scored: pd.DataFrame, summary: dict) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    scored.to_csv(REPORTS_DIR / "readiness_scores.csv", index=False)
    (REPORTS_DIR / "executive_readiness_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )


def run_pipeline() -> tuple[pd.DataFrame, dict]:
    df = load_data()
    schema_issues = validate_schema(df)
    scored = score_dataset(df)
    summary = build_summary(scored, schema_issues)
    write_reports(scored, summary)
    return scored, summary


def main() -> None:
    _, summary = run_pipeline()
    if summary["schema_issues"]:
        print("Pipeline completed with schema issues:")
        for issue in summary["schema_issues"]:
            print(f"- {issue}")
        raise SystemExit(1)

    print("Pipeline completed.")
    print(f"Average readiness score: {summary['average_readiness_score']}")
    print(f"Blocked workflows: {summary['blocked_count']}")


if __name__ == "__main__":
    main()
