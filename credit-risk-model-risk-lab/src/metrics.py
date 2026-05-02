from __future__ import annotations

import numpy as np
from sklearn import metrics as sk_metrics


def gini_from_auc(roc_auc: float) -> float:
    return 2.0 * roc_auc - 1.0


def ks_statistic(y_true: np.ndarray, y_score: np.ndarray) -> float:
    fpr, tpr, _ = sk_metrics.roc_curve(y_true, y_score)
    return float(np.max(tpr - fpr))


def expected_calibration_error(y_true: np.ndarray, y_score: np.ndarray, bins: int = 10) -> float:
    edges = np.linspace(0.0, 1.0, bins + 1)
    ece = 0.0
    for low, high in zip(edges[:-1], edges[1:]):
        if high == 1.0:
            mask = (y_score >= low) & (y_score <= high)
        else:
            mask = (y_score >= low) & (y_score < high)
        if not np.any(mask):
            continue
        observed = float(np.mean(y_true[mask]))
        predicted = float(np.mean(y_score[mask]))
        ece += float(np.mean(mask)) * abs(observed - predicted)
    return ece


def calibration_bins(y_true: np.ndarray, y_score: np.ndarray, bins: int = 10) -> list[dict[str, float]]:
    edges = np.linspace(0.0, 1.0, bins + 1)
    rows: list[dict[str, float]] = []
    for index, (low, high) in enumerate(zip(edges[:-1], edges[1:]), start=1):
        if high == 1.0:
            mask = (y_score >= low) & (y_score <= high)
        else:
            mask = (y_score >= low) & (y_score < high)
        count = int(np.sum(mask))
        rows.append(
            {
                "bin": index,
                "low": round(float(low), 4),
                "high": round(float(high), 4),
                "count": count,
                "mean_score": round(float(np.mean(y_score[mask])) if count else 0.0, 6),
                "event_rate": round(float(np.mean(y_true[mask])) if count else 0.0, 6),
            }
        )
    return rows


def population_stability_index(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> dict[str, object]:
    quantiles = np.linspace(0.0, 1.0, bins + 1)
    edges = np.unique(np.quantile(expected, quantiles))
    if len(edges) < 3:
        edges = np.linspace(float(np.min(expected)), float(np.max(expected)), bins + 1)
    edges[0] = -np.inf
    edges[-1] = np.inf

    expected_counts, _ = np.histogram(expected, bins=edges)
    actual_counts, _ = np.histogram(actual, bins=edges)
    expected_pct = np.maximum(expected_counts / max(1, len(expected)), 1e-6)
    actual_pct = np.maximum(actual_counts / max(1, len(actual)), 1e-6)
    contributions = (actual_pct - expected_pct) * np.log(actual_pct / expected_pct)
    return {
        "psi": round(float(np.sum(contributions)), 6),
        "bins": [
            {
                "bin": int(index + 1),
                "expected_pct": round(float(expected_pct[index]), 6),
                "actual_pct": round(float(actual_pct[index]), 6),
                "contribution": round(float(contributions[index]), 6),
            }
            for index in range(len(contributions))
        ],
    }


def classification_metrics(y_true: np.ndarray, y_score: np.ndarray, threshold: float = 0.5) -> dict[str, object]:
    y_pred = (y_score >= threshold).astype(int)
    roc_auc = float(sk_metrics.roc_auc_score(y_true, y_score))
    precision, recall, f1, _ = sk_metrics.precision_recall_fscore_support(
        y_true,
        y_pred,
        average="binary",
        zero_division=0,
    )
    tn, fp, fn, tp = sk_metrics.confusion_matrix(y_true, y_pred).ravel()
    return {
        "rows": int(len(y_true)),
        "event_rate": round(float(np.mean(y_true)), 6),
        "threshold": threshold,
        "roc_auc": round(roc_auc, 6),
        "pr_auc": round(float(sk_metrics.average_precision_score(y_true, y_score)), 6),
        "gini": round(gini_from_auc(roc_auc), 6),
        "ks_statistic": round(ks_statistic(y_true, y_score), 6),
        "brier_score": round(float(sk_metrics.brier_score_loss(y_true, y_score)), 6),
        "expected_calibration_error": round(expected_calibration_error(y_true, y_score), 6),
        "precision": round(float(precision), 6),
        "recall": round(float(recall), 6),
        "f1": round(float(f1), 6),
        "confusion_matrix": {
            "true_negative": int(tn),
            "false_positive": int(fp),
            "false_negative": int(fn),
            "true_positive": int(tp),
        },
    }


def threshold_operating_points(
    y_true: np.ndarray,
    y_score: np.ndarray,
    thresholds: tuple[float, ...] = (0.05, 0.1, 0.15, 0.2, 0.3, 0.5),
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for threshold in thresholds:
        y_pred = (y_score >= threshold).astype(int)
        tn, fp, fn, tp = sk_metrics.confusion_matrix(y_true, y_pred).ravel()
        reviewed = int(tp + fp)
        precision = tp / reviewed if reviewed else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        false_positive_rate = fp / (fp + tn) if (fp + tn) else 0.0
        rows.append(
            {
                "threshold": round(float(threshold), 4),
                "review_rate": round(float(reviewed / len(y_true)), 6),
                "precision": round(float(precision), 6),
                "recall": round(float(recall), 6),
                "false_positive_rate": round(float(false_positive_rate), 6),
                "true_positive": int(tp),
                "false_positive": int(fp),
                "false_negative": int(fn),
                "true_negative": int(tn),
            }
        )
    return rows
