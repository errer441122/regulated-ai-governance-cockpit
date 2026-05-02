from __future__ import annotations

import argparse
import json
import os
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import psutil
import torch
import yaml
from datasets import load_dataset
from sklearn.metrics import accuracy_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer


@dataclass(frozen=True)
class BenchmarkConfig:
    model_dir: str = "artifacts/model"
    dataset_name: str = "evalitahf/sentiment_analysis"
    text_column: str = "text"
    onnx_path: str = "artifacts/model/model.onnx"
    quantized_onnx_path: str = "artifacts/model/model-quantized.onnx"
    max_length: int = 128
    batch_size: int = 16
    warmup_batches: int = 3
    measured_batches: int = 20
    report_json: str = "reports/profiling_report.json"
    report_md: str = "reports/optimization_report.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark PyTorch, torch.compile, ONNX Runtime and quantized ONNX.")
    parser.add_argument("--config", default="configs/optimize.yaml")
    parser.add_argument("--cpu", action="store_true", help="Force CPU execution for PyTorch engines.")
    return parser.parse_args()


def load_config(path: str) -> BenchmarkConfig:
    with open(path, "r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    config_fields = BenchmarkConfig.__dataclass_fields__.keys()
    filtered = {key: value for key, value in raw.items() if key in config_fields}
    return BenchmarkConfig(**filtered)


def sentipolc_label(example: dict[str, int]) -> int:
    positive = int(example.get("opos", example.get("positive", 0)))
    negative = int(example.get("oneg", example.get("negative", 0)))
    if positive == 1 and negative == 0:
        return 1
    if negative == 1 and positive == 0:
        return 0
    return 2


def load_eval_texts(config: BenchmarkConfig) -> tuple[list[str], list[int]]:
    raw = load_dataset(config.dataset_name)
    split_name = "validation" if "validation" in raw else "test" if "test" in raw else "train"
    dataset = raw[split_name].select(range(min(len(raw[split_name]), config.batch_size * config.measured_batches)))
    texts = [str(item[config.text_column]) for item in dataset]
    labels = [sentipolc_label(item) for item in dataset]
    return texts, labels


def batches(texts: list[str], batch_size: int) -> list[list[str]]:
    return [texts[index : index + batch_size] for index in range(0, len(texts), batch_size)]


def memory_mb() -> float:
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)


def benchmark_engine(
    name: str,
    predict_fn: Callable[[list[str]], np.ndarray],
    text_batches: list[list[str]],
    labels: list[int],
    warmup_batches: int,
) -> dict[str, float | str]:
    for batch in text_batches[:warmup_batches]:
        predict_fn(batch)

    latencies: list[float] = []
    predictions: list[int] = []
    before_memory = memory_mb()
    start_total = time.perf_counter()
    for batch in text_batches[warmup_batches:]:
        start = time.perf_counter()
        batch_predictions = predict_fn(batch)
        latencies.append((time.perf_counter() - start) * 1000)
        predictions.extend(batch_predictions.astype(int).tolist())
    elapsed = time.perf_counter() - start_total
    after_memory = memory_mb()

    measured_labels = labels[warmup_batches * len(text_batches[0]) : warmup_batches * len(text_batches[0]) + len(predictions)]
    return {
        "engine": name,
        "accuracy": float(accuracy_score(measured_labels, predictions)) if predictions else 0.0,
        "latency_p50_ms": float(statistics.median(latencies)) if latencies else 0.0,
        "latency_p95_ms": float(np.percentile(latencies, 95)) if latencies else 0.0,
        "throughput_samples_s": float(len(predictions) / elapsed) if elapsed > 0 else 0.0,
        "memory_delta_mb": float(after_memory - before_memory),
    }


def make_torch_predictor(model_dir: str, max_length: int, compile_model: bool, force_cpu: bool) -> Callable[[list[str]], np.ndarray]:
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    device = torch.device("cpu" if force_cpu or not torch.cuda.is_available() else "cuda")
    model.to(device).eval()
    if compile_model:
        model = torch.compile(model, mode="reduce-overhead")

    def predict(texts: list[str]) -> np.ndarray:
        encoded = tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )
        encoded = {key: value.to(device) for key, value in encoded.items()}
        with torch.no_grad():
            logits = model(**encoded).logits
        return torch.argmax(logits, dim=-1).detach().cpu().numpy()

    return predict


def make_onnx_predictor(model_path: str, tokenizer_dir: str, max_length: int) -> Callable[[list[str]], np.ndarray]:
    import onnxruntime as ort

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
    session = ort.InferenceSession(model_path, providers=ort.get_available_providers())
    input_names = {input_meta.name for input_meta in session.get_inputs()}

    def predict(texts: list[str]) -> np.ndarray:
        encoded = tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="np",
        )
        inputs = {
            key: value.astype(np.int64)
            for key, value in encoded.items()
            if key in input_names
        }
        logits = session.run(None, inputs)[0]
        return np.argmax(logits, axis=-1)

    return predict


def write_markdown_report(path: str, results: list[dict[str, float | str]]) -> None:
    rows = "\n".join(
        f"| {item['engine']} | {item['accuracy']:.4f} | {item['latency_p50_ms']:.2f} | "
        f"{item['latency_p95_ms']:.2f} | {item['throughput_samples_s']:.2f} | {item['memory_delta_mb']:.2f} |"
        for item in results
    )
    content = f"""# Optimization Report

This report is generated by `src/benchmark.py` after fine-tuning and ONNX export.

| Engine | Accuracy | p50 latency ms | p95 latency ms | Throughput samples/s | Memory delta MB |
| --- | ---: | ---: | ---: | ---: | ---: |
{rows}

Interpretation:

- PyTorch eager is the baseline for functional parity.
- `torch.compile` captures PyTorch graph-level optimization on the same checkpoint.
- ONNX Runtime measures portable inference execution.
- ONNX dynamic quantization measures CPU-friendly compression and latency effects.
"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    texts, labels = load_eval_texts(config)
    text_batches = batches(texts, config.batch_size)

    engines = [
        ("pytorch_eager", make_torch_predictor(config.model_dir, config.max_length, False, args.cpu)),
        ("torch_compile", make_torch_predictor(config.model_dir, config.max_length, True, args.cpu)),
        ("onnxruntime", make_onnx_predictor(config.onnx_path, config.model_dir, config.max_length)),
        ("onnxruntime_quantized", make_onnx_predictor(config.quantized_onnx_path, config.model_dir, config.max_length)),
    ]
    results = [
        benchmark_engine(name, predictor, text_batches, labels, config.warmup_batches)
        for name, predictor in engines
    ]

    Path(config.report_json).parent.mkdir(parents=True, exist_ok=True)
    Path(config.report_json).write_text(json.dumps({"results": results}, indent=2), encoding="utf-8")
    write_markdown_report(config.report_md, results)
    print(json.dumps({"results": results}, indent=2))


if __name__ == "__main__":
    main()

