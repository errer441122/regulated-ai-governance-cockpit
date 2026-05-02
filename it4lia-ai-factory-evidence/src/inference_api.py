from __future__ import annotations

import os
import time
from typing import Protocol, Sequence

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class SentimentPrediction(BaseModel):
    label: str
    score: float
    class_id: int
    backend: str
    latency_ms: float


class PredictRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1, max_length=64)


class PredictResponse(BaseModel):
    predictions: list[SentimentPrediction]


class PredictionBackend(Protocol):
    def predict(self, texts: Sequence[str]) -> list[SentimentPrediction]:
        ...


def _softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits, axis=-1, keepdims=True)
    exp = np.exp(shifted)
    return exp / np.sum(exp, axis=-1, keepdims=True)


class TorchPipelineBackend:
    def __init__(self, model_dir: str, device: int = -1) -> None:
        from transformers import pipeline

        self.pipeline = pipeline(
            "text-classification",
            model=model_dir,
            tokenizer=model_dir,
            device=device,
            top_k=None,
            truncation=True,
        )

    def predict(self, texts: Sequence[str]) -> list[SentimentPrediction]:
        start = time.perf_counter()
        outputs = self.pipeline(list(texts))
        elapsed_ms = (time.perf_counter() - start) * 1000
        per_item_ms = elapsed_ms / max(1, len(texts))

        predictions: list[SentimentPrediction] = []
        for item in outputs:
            best = max(item, key=lambda record: record["score"])
            class_id = int(str(best["label"]).split("_")[-1]) if "_" in best["label"] else 0
            predictions.append(
                SentimentPrediction(
                    label=str(best["label"]).lower(),
                    score=float(best["score"]),
                    class_id=class_id,
                    backend="pytorch-eager",
                    latency_ms=round(per_item_ms, 3),
                )
            )
        return predictions


class OnnxRuntimeBackend:
    def __init__(
        self,
        model_path: str,
        tokenizer_dir: str,
        max_length: int = 128,
        providers: Sequence[str] | None = None,
    ) -> None:
        import onnxruntime as ort
        from transformers import AutoTokenizer

        self.session = ort.InferenceSession(
            model_path,
            providers=list(providers or ort.get_available_providers()),
        )
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
        self.max_length = max_length
        self.input_names = {input_meta.name for input_meta in self.session.get_inputs()}
        self.labels = {0: "negative", 1: "positive", 2: "neutral"}

    def predict(self, texts: Sequence[str]) -> list[SentimentPrediction]:
        encoded = self.tokenizer(
            list(texts),
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="np",
        )
        inputs = {
            name: value.astype(np.int64)
            for name, value in encoded.items()
            if name in self.input_names
        }

        start = time.perf_counter()
        logits = self.session.run(None, inputs)[0]
        elapsed_ms = (time.perf_counter() - start) * 1000
        probabilities = _softmax(logits)
        class_ids = np.argmax(probabilities, axis=-1)
        per_item_ms = elapsed_ms / max(1, len(texts))

        return [
            SentimentPrediction(
                label=self.labels.get(int(class_id), f"label_{int(class_id)}"),
                score=float(probabilities[row_idx, class_id]),
                class_id=int(class_id),
                backend="onnxruntime",
                latency_ms=round(per_item_ms, 3),
            )
            for row_idx, class_id in enumerate(class_ids)
        ]


def load_backend_from_env() -> PredictionBackend:
    backend_name = os.getenv("IT4LIA_BACKEND", "onnx").lower()
    model_dir = os.getenv("IT4LIA_MODEL_DIR", "artifacts/model")
    onnx_path = os.getenv("IT4LIA_ONNX_MODEL", "artifacts/model/model-quantized.onnx")
    max_length = int(os.getenv("IT4LIA_MAX_LENGTH", "128"))

    if backend_name == "onnx":
        return OnnxRuntimeBackend(
            model_path=onnx_path,
            tokenizer_dir=model_dir,
            max_length=max_length,
        )

    device = int(os.getenv("IT4LIA_TORCH_DEVICE", "-1"))
    return TorchPipelineBackend(model_dir=model_dir, device=device)


def create_app(backend: PredictionBackend | None = None) -> FastAPI:
    app = FastAPI(
        title="IT4LIA Italian Sentiment Inference API",
        version="0.1.0",
        description="Minimal FastAPI wrapper for optimized Italian BERT sentiment inference.",
    )
    state: dict[str, PredictionBackend | None] = {"backend": backend}

    def get_backend() -> PredictionBackend:
        if state["backend"] is None:
            state["backend"] = load_backend_from_env()
        return state["backend"]

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/predict", response_model=PredictResponse)
    def predict(request: PredictRequest) -> PredictResponse:
        texts = [text.strip() for text in request.texts]
        if any(not text for text in texts):
            raise HTTPException(status_code=422, detail="All texts must be non-empty.")
        predictions = get_backend().predict(texts)
        return PredictResponse(predictions=predictions)

    return app


app = create_app()
