from __future__ import annotations

import io
import sys
from pathlib import Path

from PIL import Image


LAB_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = LAB_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from inference_api import score_image_bytes


def _image_bytes(color: tuple[int, int, int]) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (32, 32), color=color).save(buffer, format="PNG")
    return buffer.getvalue()


def test_score_image_bytes_returns_documented_fallback_when_checkpoint_is_missing(tmp_path: Path) -> None:
    result = score_image_bytes(
        _image_bytes((240, 30, 30)),
        model_path=tmp_path / "missing_model.pt",
        threshold=0.5,
    )

    assert result["model_status"] == "fallback_untrained"
    assert result["predicted_label"] in {"normal", "anomaly"}
    assert 0.0 <= result["anomaly_probability"] <= 1.0
    assert result["decision_boundary"] == "portfolio demo only; no automated quality decision"
