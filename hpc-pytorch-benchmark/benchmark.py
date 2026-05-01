from __future__ import annotations

import argparse
import json
import platform
import time
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = BASE_DIR / "artifacts"


def _run_numpy(quick: bool) -> dict[str, Any]:
    import numpy as np

    rng = np.random.default_rng(42)
    rows = 256 if quick else 1024
    features = 24
    x = rng.normal(size=(rows, features))
    weights = rng.normal(size=(features, 1))
    y = (x @ weights > 0).astype(float)
    started = time.perf_counter()
    for _ in range(12 if quick else 60):
        logits = x @ weights
        preds = 1 / (1 + np.exp(-logits))
        grad = x.T @ (preds - y) / rows
        weights -= 0.1 * grad
    train_seconds = time.perf_counter() - started
    infer_started = time.perf_counter()
    _ = 1 / (1 + np.exp(-(x[:32] @ weights)))
    inference_ms = (time.perf_counter() - infer_started) * 1000
    return {
        "backend": "numpy_fallback_no_torch",
        "rows": rows,
        "features": features,
        "runtime_seconds": round(train_seconds, 4),
        "inference_latency_ms": round(inference_ms, 4),
        "execution_note": "Executed locally on CPU with NumPy fallback because PyTorch is optional in CI.",
    }


def _run_torch(quick: bool) -> dict[str, Any]:
    import torch

    torch.manual_seed(42)
    rows = 256 if quick else 1024
    features = 24
    x = torch.randn(rows, features)
    y = (torch.sum(x[:, :4], dim=1, keepdim=True) > 0).float()
    model = torch.nn.Sequential(torch.nn.Linear(features, 16), torch.nn.ReLU(), torch.nn.Linear(16, 1))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = torch.nn.BCEWithLogitsLoss()
    started = time.perf_counter()
    for _ in range(8 if quick else 40):
        optimizer.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        optimizer.step()
    train_seconds = time.perf_counter() - started
    infer_started = time.perf_counter()
    with torch.no_grad():
        _ = torch.sigmoid(model(x[:32]))
    inference_ms = (time.perf_counter() - infer_started) * 1000
    return {
        "backend": f"pytorch_{torch.__version__}",
        "rows": rows,
        "features": features,
        "runtime_seconds": round(train_seconds, 4),
        "inference_latency_ms": round(inference_ms, 4),
        "execution_note": "Executed locally on CPU. Slurm script provided as portability artifact; no real HPC/GPU claim.",
    }


def run(quick: bool = False) -> dict[str, Any]:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        payload = _run_torch(quick)
    except ModuleNotFoundError:
        payload = _run_numpy(quick)
    payload.update(
        {
            "hardware_note": platform.platform(),
            "gpu_benchmark_optional": "not executed",
            "boundary": "No CINECA, IT4LIA, Leonardo, or GPU execution claim.",
        }
    )
    (ARTIFACT_DIR / "cpu_benchmark.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    (ARTIFACT_DIR / "gpu_benchmark_optional.json").write_text(
        json.dumps({"status": "not_executed", "boundary": payload["boundary"]}, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "training_log.txt").write_text(
        f"backend={payload['backend']} runtime_seconds={payload['runtime_seconds']}\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "inference_latency_report.md").write_text(
        "# Inference Latency Report\n\n"
        f"Backend: `{payload['backend']}`\n\n"
        f"Latency: `{payload['inference_latency_ms']}` ms for 32 records.\n\n"
        f"Execution note: {payload['execution_note']}\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "model_card.md").write_text(
        "# HPC PyTorch Benchmark Model Card\n\n"
        "Task: tiny binary classifier benchmark for local CPU evidence.\n\n"
        f"Backend: `{payload['backend']}`\n\n"
        "Out of scope: production AI, real HPC execution, distributed training, or GPU performance claim.\n",
        encoding="utf-8",
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(quick=args.quick), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
