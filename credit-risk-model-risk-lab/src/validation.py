from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.inspection import permutation_importance


def _markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows available._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def proxy_variable_notes(feature_columns: list[str]) -> list[dict[str, str]]:
    reviews = {
        "age": {
            "risk_area": "demographic proxy",
            "review_note": "Potential protected-class proxy. Keep for transparent benchmark comparison only; do not use for automated production decisions without legal, fairness, and policy review.",
            "action": "Monitor score distribution by age bands where lawful; assess alternate models with and without this feature.",
        },
        "monthlyincome": {
            "risk_area": "socioeconomic proxy",
            "review_note": "Income can proxy socioeconomic status and data availability. Missingness can itself become a protected-class proxy.",
            "action": "Track missingness, imputation impact, and feature contribution over time.",
        },
        "debtratio": {
            "risk_area": "affordability proxy",
            "review_note": "Debt ratio is domain-relevant but can amplify historical access-to-credit patterns.",
            "action": "Compare calibration and error rates across documented affordability bands.",
        },
        "numberofdependents": {
            "risk_area": "household-composition proxy",
            "review_note": "Household composition may be a sensitive-context proxy depending on jurisdiction and policy use.",
            "action": "Use only with explicit policy approval and monitor missingness/imputation impact.",
        },
        "numberrealestateloansorlines": {
            "risk_area": "wealth / asset proxy",
            "review_note": "Property-related variables can proxy wealth and local housing-market access.",
            "action": "Review stability by macro period and document any segment-level degradation.",
        },
    }

    rows: list[dict[str, str]] = []
    for feature in feature_columns:
        key = feature.lower()
        if key in reviews:
            rows.append({"feature": feature, **reviews[key]})
    return rows


def monitoring_plan() -> list[dict[str, str]]:
    return [
        {
            "control": "Input data quality",
            "metric": "missingness, range violations, imputation rate",
            "trigger": "material movement from training baseline",
        },
        {
            "control": "Score drift",
            "metric": "monthly PSI and score-band volume",
            "trigger": "PSI above 0.10 for review, above 0.25 for escalation",
        },
        {
            "control": "Calibration",
            "metric": "Brier score and expected calibration error",
            "trigger": "worse than validation baseline for two reporting periods",
        },
        {
            "control": "Threshold behavior",
            "metric": "review rate, precision, recall, false-positive rate",
            "trigger": "policy threshold no longer meets agreed human-review capacity",
        },
        {
            "control": "Proxy/fairness watch",
            "metric": "lawful segment-level error and calibration review",
            "trigger": "statistically meaningful degradation in a documented segment",
        },
    ]


def permutation_importance_rows(
    model: Any,
    x: np.ndarray,
    y: np.ndarray,
    feature_names: list[str],
    n_repeats: int = 3,
    random_state: int = 42,
) -> list[dict[str, object]]:
    result = permutation_importance(
        model,
        x,
        y,
        scoring="roc_auc",
        n_repeats=n_repeats,
        random_state=random_state,
        n_jobs=1,
    )
    rows = [
        {
            "feature": feature,
            "importance_mean": round(float(mean), 6),
            "importance_std": round(float(std), 6),
        }
        for feature, mean, std in zip(feature_names, result.importances_mean, result.importances_std)
    ]
    rows.sort(key=lambda row: row["importance_mean"], reverse=True)
    return [{"rank": index + 1, **row} for index, row in enumerate(rows)]


def _model_comparison_rows(training_summary: dict[str, Any]) -> list[dict[str, object]]:
    candidate_metrics = training_summary.get("candidate_metrics", {})
    rows: list[dict[str, object]] = []
    for name, values in candidate_metrics.items():
        rows.append(
            {
                "model": name,
                "roc_auc": values.get("roc_auc", ""),
                "pr_auc": values.get("pr_auc", ""),
                "brier_score": values.get("brier_score", ""),
                "selected": "yes" if name == training_summary.get("selected_model") else "no",
            }
        )
    return rows


def render_validation_report(
    metrics: dict[str, Any],
    psi: dict[str, Any],
    thresholds: list[dict[str, Any]],
    feature_importance: list[dict[str, Any]],
    proxy_notes: list[dict[str, str]],
    production_monitoring: list[dict[str, str]],
    training_summary: dict[str, Any],
) -> str:
    return (
        "# Credit-Risk Validation Report\n\n"
        "This report documents the public-data validation evidence for the GiveMeSomeCredit portfolio baseline. "
        "It is model-risk practice evidence, not a production validation sign-off.\n\n"
        "## Train/Test Split And Feature Engineering\n\n"
        "- Split: stratified 80/20 holdout with random state 42.\n"
        "- Missing numeric values are median-imputed inside the model pipeline.\n"
        "- Logistic regression uses standard scaling; the tree baseline uses raw numeric features after imputation.\n"
        "- The target is `FinancialDistressNextTwoYears`, a public competition label and not an observed approval/decline population.\n\n"
        "## Model Comparison\n\n"
        + _markdown_table(_model_comparison_rows(training_summary), ["model", "roc_auc", "pr_auc", "brier_score", "selected"])
        + "\n\n"
        "## Calibration And Drift\n\n"
        f"- ROC-AUC: `{metrics.get('roc_auc')}`\n"
        f"- PR-AUC: `{metrics.get('pr_auc')}`\n"
        f"- Brier score: `{metrics.get('brier_score')}`\n"
        f"- Expected calibration error: `{metrics.get('expected_calibration_error')}`\n"
        f"- Train/test score PSI: `{psi.get('psi')}`\n\n"
        "## Threshold Selection\n\n"
        "Thresholds are treated as review-capacity scenarios, not approval or denial rules.\n\n"
        + _markdown_table(thresholds, ["threshold", "review_rate", "precision", "recall"])
        + "\n\n"
        "## Explainability Evidence\n\n"
        + _markdown_table(feature_importance, ["rank", "feature", "importance_mean", "importance_std"])
        + "\n\n"
        "## Proxy / Fairness Review\n\n"
        + _markdown_table(proxy_notes, ["feature", "risk_area", "review_note", "action"])
        + "\n\n"
        "## Reject-Inference Boundary\n\n"
        "The public dataset contains observed distress labels for the competition population, but it does not provide a real lender's rejected-applicant population, policy rules, or application-time decision path. "
        "A production credit-risk validation would need reject-inference analysis, challenger assumptions, approval-policy context, and independent review before any model could influence credit decisions.\n\n"
        "## Production Monitoring Plan\n\n"
        + _markdown_table(production_monitoring, ["control", "metric", "trigger"])
        + "\n\n"
        "## Validation Decision\n\n"
        "Acceptable as portfolio evidence for credit-risk modelling, calibration, drift, explainability, threshold discussion, and model-risk documentation. "
        "Not acceptable for production lending, automated decisions, or regulatory compliance claims.\n"
    )
