from __future__ import annotations

import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from PIL import Image


try:
    import torch
    from torch import nn
    from torch.utils.data import Dataset

    TORCH_AVAILABLE = True
except ImportError:  # pragma: no cover - local docs can be read without torch
    torch = None
    nn = None
    Dataset = object
    TORCH_AVAILABLE = False


IMAGE_SUFFIXES = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff"}
CLASS_NAMES = ["normal", "anomaly"]


@dataclass(frozen=True)
class ImageRecord:
    path: Path
    category: str
    split: str
    defect_type: str
    label: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": str(self.path),
            "category": self.category,
            "split": self.split,
            "defect_type": self.defect_type,
            "label": self.label,
        }


def _iter_image_files(folder: Path) -> Iterable[Path]:
    for path in sorted(folder.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            yield path


def discover_mvtec_records(data_dir: str | Path, split: str) -> list[ImageRecord]:
    """Discover a MVTec-style image tree.

    Expected layout: category/split/defect_type/image.png. The `good`
    defect type is label 0; every other folder is label 1.
    """

    root = Path(data_dir)
    if not root.exists():
        raise FileNotFoundError(f"Dataset root does not exist: {root}")

    records: list[ImageRecord] = []
    for category_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        split_dir = category_dir / split
        if not split_dir.is_dir():
            continue
        for defect_dir in sorted(path for path in split_dir.iterdir() if path.is_dir()):
            label = 0 if defect_dir.name == "good" else 1
            for image_path in _iter_image_files(defect_dir):
                records.append(
                    ImageRecord(
                        path=image_path,
                        category=category_dir.name,
                        split=split,
                        defect_type=defect_dir.name,
                        label=label,
                    )
                )

    if not records:
        raise ValueError(
            "No images found. Expected layout like "
            f"{root}/bottle/{split}/good/*.png and defect folders beside good/."
        )
    return records


def class_counts(records: Iterable[ImageRecord]) -> dict[str, Any]:
    normal = 0
    anomaly = 0
    defect_types: dict[str, int] = {}
    categories: dict[str, int] = {}
    for record in records:
        normal += int(record.label == 0)
        anomaly += int(record.label == 1)
        defect_types[record.defect_type] = defect_types.get(record.defect_type, 0) + 1
        categories[record.category] = categories.get(record.category, 0) + 1
    return {
        "normal": normal,
        "anomaly": anomaly,
        "defect_types": dict(sorted(defect_types.items())),
        "categories": dict(sorted(categories.items())),
    }


def ensure_binary_labels(records: list[ImageRecord], context: str) -> None:
    labels = {record.label for record in records}
    if labels != {0, 1}:
        counts = class_counts(records)
        raise ValueError(
            f"{context} needs both normal and anomaly images for supervised training/evaluation. "
            f"Observed counts: normal={counts['normal']}, anomaly={counts['anomaly']}."
        )


def require_torch() -> None:
    if not TORCH_AVAILABLE:
        raise RuntimeError("PyTorch is required for training, evaluation, and checkpoint-backed inference.")


def resolve_device(device: str) -> Any:
    require_torch()
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    return torch.device(device)


def image_to_tensor(image: Image.Image, image_size: int) -> Any:
    require_torch()
    resized = image.convert("RGB").resize((image_size, image_size))
    array = np.asarray(resized, dtype=np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    normalized = (array - mean) / std
    return torch.from_numpy(normalized.transpose(2, 0, 1)).float()


def load_image_tensor(path: str | Path, image_size: int) -> Any:
    with Image.open(path) as image:
        return image_to_tensor(image, image_size)


def image_bytes_to_tensor(image_bytes: bytes, image_size: int) -> Any:
    with Image.open(io.BytesIO(image_bytes)) as image:
        return image_to_tensor(image, image_size)


class MVTecImageDataset(Dataset):
    def __init__(self, records: list[ImageRecord], image_size: int):
        self.records = records
        self.image_size = image_size

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> tuple[Any, int]:
        record = self.records[index]
        return load_image_tensor(record.path, self.image_size), record.label


if TORCH_AVAILABLE:

    class TinyDefectCNN(nn.Module):
        def __init__(self, num_classes: int = 2):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(3, 12, kernel_size=3, padding=1),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(2),
                nn.Conv2d(12, 24, kernel_size=3, padding=1),
                nn.ReLU(inplace=True),
                nn.AdaptiveAvgPool2d((1, 1)),
            )
            self.classifier = nn.Linear(24, num_classes)

        def forward(self, inputs: Any) -> Any:
            features = self.features(inputs)
            return self.classifier(features.flatten(1))

else:

    class TinyDefectCNN:  # pragma: no cover
        pass


def build_model(architecture: str, num_classes: int = 2, pretrained: bool = False) -> Any:
    require_torch()
    normalized = architecture.lower()
    if normalized == "tiny-cnn":
        return TinyDefectCNN(num_classes=num_classes)

    if normalized == "resnet18":
        try:
            from torchvision import models
        except Exception as exc:  # pragma: no cover - depends on optional package
            raise RuntimeError(
                "ResNet18 requires torchvision. Install it for the real MVTec training path, "
                "or use --architecture tiny-cnn for local smoke tests."
            ) from exc

        weights = None
        if pretrained:
            try:
                weights = models.ResNet18_Weights.DEFAULT
            except AttributeError:  # pragma: no cover - older torchvision
                weights = "DEFAULT"
        try:
            model = models.resnet18(weights=weights)
        except TypeError:  # pragma: no cover - older torchvision
            model = models.resnet18(pretrained=pretrained)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        return model

    raise ValueError(f"Unsupported architecture: {architecture}. Use 'resnet18' or 'tiny-cnn'.")


def save_checkpoint(model: Any, path: str | Path, metadata: dict[str, Any]) -> None:
    require_torch()
    checkpoint_path = Path(path)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "metadata": metadata,
        },
        checkpoint_path,
    )


def _torch_load(path: Path, map_location: Any) -> dict[str, Any]:
    try:
        return torch.load(path, map_location=map_location, weights_only=False)
    except TypeError:  # pragma: no cover - older torch
        return torch.load(path, map_location=map_location)


def load_checkpoint(path: str | Path, map_location: str | Any = "cpu") -> tuple[Any, dict[str, Any]]:
    require_torch()
    checkpoint_path = Path(path)
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint does not exist: {checkpoint_path}")

    payload = _torch_load(checkpoint_path, map_location=map_location)
    metadata = dict(payload.get("metadata", {}))
    architecture = str(metadata.get("architecture", "resnet18"))
    model = build_model(
        architecture=architecture,
        num_classes=int(metadata.get("num_classes", 2)),
        pretrained=False,
    )
    model.load_state_dict(payload["model_state_dict"])
    model.eval()
    return model, metadata


def save_json(payload: dict[str, Any], path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, default=_json_default) + "\n", encoding="utf-8")


def _json_default(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")
