from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw


LAB_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = LAB_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from evaluate import evaluate_model
from train import train_model


def _write_normal(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (32, 32), color=(35, 35, 35)).save(path)


def _write_defect(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (32, 32), color=(35, 35, 35))
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 10, 22, 22), fill=(230, 40, 40))
    image.save(path)


def _build_tiny_mvtec_tree(root: Path) -> None:
    for split in ("train", "test"):
        for index in range(2):
            _write_normal(root / "bottle" / split / "good" / f"normal_{index}.png")
            _write_defect(root / "bottle" / split / "crack" / f"defect_{index}.png")


def test_train_and_evaluate_smoke_pipeline_writes_checkpoint_and_metrics(tmp_path: Path) -> None:
    dataset_root = tmp_path / "mvtec_subset"
    output_dir = tmp_path / "artifacts"
    _build_tiny_mvtec_tree(dataset_root)

    train_summary = train_model(
        data_dir=dataset_root,
        output_dir=output_dir,
        architecture="tiny-cnn",
        epochs=1,
        batch_size=2,
        image_size=32,
        learning_rate=0.001,
        device="cpu",
    )

    checkpoint_path = Path(train_summary["checkpoint_path"])
    assert checkpoint_path.exists()
    assert train_summary["architecture"] == "tiny-cnn"
    assert train_summary["train_records"] == 4

    metrics = evaluate_model(
        data_dir=dataset_root,
        checkpoint_path=checkpoint_path,
        output_dir=output_dir,
        split="test",
        device="cpu",
    )

    assert metrics["records"] == 4
    assert metrics["class_counts"]["normal"] == 2
    assert metrics["class_counts"]["anomaly"] == 2
    assert {"auroc", "precision", "recall", "f1", "accuracy"}.issubset(metrics)
    assert (output_dir / "evaluation_metrics.json").exists()
