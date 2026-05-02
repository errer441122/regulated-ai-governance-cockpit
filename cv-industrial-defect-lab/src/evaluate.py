from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from defect_core import (
    MVTecImageDataset,
    class_counts,
    discover_mvtec_records,
    load_checkpoint,
    resolve_device,
    save_json,
    torch,
)


def _safe_auroc(y_true: list[int], y_score: list[float]) -> float | None:
    if len(set(y_true)) < 2:
        return None
    try:
        from sklearn.metrics import roc_auc_score

        return float(roc_auc_score(y_true, y_score))
    except Exception:
        return None


def _binary_metrics(y_true: list[int], y_score: list[float], threshold: float) -> dict[str, Any]:
    predictions = [1 if score >= threshold else 0 for score in y_score]
    tp = sum(1 for truth, pred in zip(y_true, predictions) if truth == 1 and pred == 1)
    tn = sum(1 for truth, pred in zip(y_true, predictions) if truth == 0 and pred == 0)
    fp = sum(1 for truth, pred in zip(y_true, predictions) if truth == 0 and pred == 1)
    fn = sum(1 for truth, pred in zip(y_true, predictions) if truth == 1 and pred == 0)

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    accuracy = (tp + tn) / max(len(y_true), 1)

    auroc = _safe_auroc(y_true, y_score)
    return {
        "accuracy": round(float(accuracy), 6),
        "auroc": None if auroc is None else round(float(auroc), 6),
        "confusion_matrix": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
        "f1": round(float(f1), 6),
        "precision": round(float(precision), 6),
        "recall": round(float(recall), 6),
    }


def _predict_scores(
    model: Any,
    records: list[Any],
    image_size: int,
    batch_size: int,
    device_obj: Any,
) -> tuple[list[int], list[float]]:
    dataset = MVTecImageDataset(records, image_size=image_size)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False)

    y_true: list[int] = []
    y_score: list[float] = []
    model.to(device_obj)
    model.eval()
    with torch.no_grad():
        for images, labels in loader:
            logits = model(images.to(device_obj))
            probabilities = torch.softmax(logits, dim=1)[:, 1].detach().cpu().numpy()
            y_true.extend(int(value) for value in labels.numpy().tolist())
            y_score.extend(float(value) for value in probabilities.tolist())
    return y_true, y_score


def evaluate_model(
    data_dir: str | Path,
    checkpoint_path: str | Path,
    output_dir: str | Path,
    split: str = "test",
    batch_size: int = 16,
    image_size: int | None = None,
    threshold: float | None = None,
    device: str = "auto",
) -> dict[str, Any]:
    device_obj = resolve_device(device)
    model, metadata = load_checkpoint(checkpoint_path, map_location=device_obj)
    resolved_image_size = int(image_size or metadata.get("image_size", 224))
    resolved_threshold = float(threshold if threshold is not None else metadata.get("threshold", 0.5))

    records = discover_mvtec_records(data_dir, split=split)
    y_true, y_score = _predict_scores(
        model=model,
        records=records,
        image_size=resolved_image_size,
        batch_size=batch_size,
        device_obj=device_obj,
    )
    metrics = _binary_metrics(y_true, y_score, threshold=resolved_threshold)

    summary = {
        **metrics,
        "architecture": metadata.get("architecture", "unknown"),
        "checkpoint_path": str(checkpoint_path),
        "class_counts": class_counts(records),
        "device": str(device_obj),
        "image_size": resolved_image_size,
        "records": len(records),
        "split": split,
        "threshold": resolved_threshold,
        "score_mean": round(float(np.mean(y_score)), 6) if y_score else None,
        "score_std": round(float(np.std(y_score)), 6) if y_score else None,
    }
    save_json(summary, Path(output_dir) / "evaluation_metrics.json")
    return summary


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate a MVTec defect checkpoint.")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--checkpoint-path", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("cv-industrial-defect-lab/artifacts"))
    parser.add_argument("--split", default="test")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--image-size", type=int, default=None)
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--device", default="auto")
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    summary = evaluate_model(**vars(args))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
