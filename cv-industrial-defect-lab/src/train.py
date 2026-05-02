from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

import numpy as np

from defect_core import (
    CLASS_NAMES,
    MVTecImageDataset,
    build_model,
    class_counts,
    discover_mvtec_records,
    ensure_binary_labels,
    resolve_device,
    save_checkpoint,
    save_json,
    torch,
)


def _set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def train_model(
    data_dir: str | Path,
    output_dir: str | Path,
    architecture: str = "resnet18",
    epochs: int = 3,
    batch_size: int = 16,
    image_size: int = 224,
    learning_rate: float = 1e-4,
    device: str = "auto",
    threshold: float = 0.5,
    seed: int = 42,
    pretrained: bool = False,
) -> dict[str, Any]:
    device_obj = resolve_device(device)
    _set_seed(seed)

    train_records = discover_mvtec_records(data_dir, split="train")
    ensure_binary_labels(train_records, context="Training split")

    dataset = MVTecImageDataset(train_records, image_size=image_size)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = build_model(architecture=architecture, num_classes=len(CLASS_NAMES), pretrained=pretrained)
    model.to(device_obj)

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    loss_history: list[float] = []
    for _epoch in range(epochs):
        model.train()
        running_loss = 0.0
        seen = 0
        for images, labels in loader:
            images = images.to(device_obj)
            labels = labels.to(device_obj).long()

            optimizer.zero_grad(set_to_none=True)
            logits = model(images)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

            batch_size_seen = int(labels.shape[0])
            running_loss += float(loss.item()) * batch_size_seen
            seen += batch_size_seen
        loss_history.append(running_loss / max(seen, 1))

    output_path = Path(output_dir)
    checkpoint_path = output_path / "model.pt"
    metadata: dict[str, Any] = {
        "architecture": architecture,
        "class_names": CLASS_NAMES,
        "dataset_root": str(Path(data_dir)),
        "image_size": image_size,
        "num_classes": len(CLASS_NAMES),
        "pretrained": pretrained,
        "threshold": threshold,
        "train_split": "train",
    }
    save_checkpoint(model, checkpoint_path, metadata)

    summary = {
        **metadata,
        "batch_size": batch_size,
        "checkpoint_path": str(checkpoint_path),
        "class_counts": class_counts(train_records),
        "device": str(device_obj),
        "epochs": epochs,
        "learning_rate": learning_rate,
        "loss_history": [round(value, 6) for value in loss_history],
        "train_records": len(train_records),
    }
    save_json(summary, output_path / "training_summary.json")
    return summary


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fine-tune a ResNet18-style defect classifier on a MVTec subset.")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("cv-industrial-defect-lab/artifacts"))
    parser.add_argument("--architecture", choices=["resnet18", "tiny-cnn"], default="resnet18")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--pretrained", action="store_true")
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    summary = train_model(**vars(args))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
