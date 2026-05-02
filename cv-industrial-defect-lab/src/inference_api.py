from __future__ import annotations

import io
import os
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

from defect_core import image_bytes_to_tensor, load_checkpoint, resolve_device, torch


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = BASE_DIR / "artifacts" / "model.pt"
DECISION_BOUNDARY = "portfolio demo only; no automated quality decision"


try:
    from fastapi import FastAPI, File, HTTPException, UploadFile
except ImportError:  # pragma: no cover - tests call helper without FastAPI
    FastAPI = None
    File = None
    HTTPException = RuntimeError
    UploadFile = object


def _fallback_score(image_bytes: bytes) -> float:
    with Image.open(io.BytesIO(image_bytes)) as image:
        grayscale = image.convert("L").resize((64, 64))
        array = np.asarray(grayscale, dtype=np.float32)
    contrast_signal = min(float(array.std()) / 96.0, 1.0)
    brightness_signal = min(abs(float(array.mean()) - 128.0) / 255.0, 1.0)
    return float(np.clip((0.75 * contrast_signal) + (0.25 * brightness_signal), 0.0, 1.0))


def score_image_bytes(
    image_bytes: bytes,
    model_path: str | Path | None = None,
    threshold: float | None = None,
    image_size: int | None = None,
    device: str = "cpu",
) -> dict[str, Any]:
    resolved_model_path = Path(model_path or os.getenv("CV_DEFECT_MODEL", str(DEFAULT_MODEL_PATH)))
    resolved_threshold = 0.5 if threshold is None else threshold

    if resolved_model_path.exists():
        device_obj = resolve_device(device)
        model, metadata = load_checkpoint(resolved_model_path, map_location=device_obj)
        resolved_image_size = int(image_size or metadata.get("image_size", 224))
        resolved_threshold = float(threshold if threshold is not None else metadata.get("threshold", resolved_threshold))
        tensor = image_bytes_to_tensor(image_bytes, resolved_image_size).unsqueeze(0).to(device_obj)
        model.to(device_obj)
        model.eval()
        with torch.no_grad():
            logits = model(tensor)
            probability = torch.softmax(logits, dim=1)[0, 1].detach().cpu().item()
        model_status = "checkpoint_loaded"
        architecture = str(metadata.get("architecture", "unknown"))
    else:
        probability = _fallback_score(image_bytes)
        model_status = "fallback_untrained"
        architecture = "heuristic-fallback"
        resolved_image_size = int(image_size or 64)

    predicted_label = "anomaly" if probability >= resolved_threshold else "normal"
    return {
        "anomaly_probability": round(float(probability), 6),
        "architecture": architecture,
        "confidence": round(float(max(probability, 1.0 - probability)), 6),
        "decision_boundary": DECISION_BOUNDARY,
        "image_size": resolved_image_size,
        "model_path": str(resolved_model_path),
        "model_status": model_status,
        "predicted_label": predicted_label,
        "threshold": round(float(resolved_threshold), 6),
    }


if FastAPI:
    app = FastAPI(title="Industrial Defect Vision API", version="1.0.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": "industrial-defect-cv-demo"}

    @app.post("/predict")
    async def predict(file: UploadFile = File(...)) -> dict[str, Any]:
        try:
            contents = await file.read()
            result = score_image_bytes(contents)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {
            **result,
            "filename": file.filename,
            "content_type": file.content_type,
        }
else:
    app = None
