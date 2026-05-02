from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import torch
import yaml
from transformers import AutoModelForSequenceClassification, AutoTokenizer


@dataclass(frozen=True)
class OptimizeConfig:
    model_dir: str = "artifacts/model"
    onnx_path: str = "artifacts/model/model.onnx"
    quantized_onnx_path: str = "artifacts/model/model-quantized.onnx"
    max_length: int = 128
    opset: int = 17
    compile_mode: str = "reduce-overhead"
    metadata_path: str = "reports/optimization_metadata.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export Italian BERT to ONNX and apply dynamic quantization.")
    parser.add_argument("--config", default="configs/optimize.yaml")
    parser.add_argument("--skip-compile-check", action="store_true")
    return parser.parse_args()


def load_config(path: str) -> OptimizeConfig:
    with open(path, "r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    known_fields = OptimizeConfig.__dataclass_fields__.keys()
    unknown = sorted(set(raw) - set(known_fields))
    if unknown:
        raise ValueError(f"Unknown config keys: {unknown}")
    return OptimizeConfig(**raw)


def export_onnx(config: OptimizeConfig) -> None:
    tokenizer = AutoTokenizer.from_pretrained(config.model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(config.model_dir)
    model.eval()

    encoded = tokenizer(
        ["Questo modello analizza sentimenti in italiano."],
        padding=True,
        truncation=True,
        max_length=config.max_length,
        return_tensors="pt",
    )
    model_inputs = {
        key: value
        for key, value in encoded.items()
        if key in {"input_ids", "attention_mask", "token_type_ids"}
    }

    Path(config.onnx_path).parent.mkdir(parents=True, exist_ok=True)
    with torch.no_grad():
        torch.onnx.export(
            model,
            tuple(model_inputs.values()),
            config.onnx_path,
            input_names=list(model_inputs.keys()),
            output_names=["logits"],
            dynamic_axes={
                name: {0: "batch", 1: "sequence"} for name in model_inputs
            }
            | {"logits": {0: "batch"}},
            opset_version=config.opset,
        )


def quantize_onnx(config: OptimizeConfig) -> None:
    from onnxruntime.quantization import QuantType, quantize_dynamic

    quantize_dynamic(
        model_input=config.onnx_path,
        model_output=config.quantized_onnx_path,
        weight_type=QuantType.QInt8,
    )


def compile_smoke_check(config: OptimizeConfig) -> dict[str, str]:
    tokenizer = AutoTokenizer.from_pretrained(config.model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(config.model_dir)
    model.eval()
    compiled = torch.compile(model, mode=config.compile_mode)
    encoded = tokenizer(
        ["Smoke test torch.compile su BERT italiano."],
        padding=True,
        truncation=True,
        max_length=config.max_length,
        return_tensors="pt",
    )
    with torch.no_grad():
        _ = compiled(**encoded)
    return {"torch_compile": "smoke_check_passed", "compile_mode": config.compile_mode}


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    metadata: dict[str, str | int] = {
        "model_dir": config.model_dir,
        "onnx_path": config.onnx_path,
        "quantized_onnx_path": config.quantized_onnx_path,
        "opset": config.opset,
    }
    if not args.skip_compile_check:
        metadata.update(compile_smoke_check(config))
    export_onnx(config)
    quantize_onnx(config)

    Path(config.metadata_path).parent.mkdir(parents=True, exist_ok=True)
    with open(config.metadata_path, "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()

