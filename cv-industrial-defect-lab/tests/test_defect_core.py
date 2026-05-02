from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


LAB_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = LAB_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from defect_core import class_counts, discover_mvtec_records


def _write_image(path: Path, color: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (24, 24), color=color).save(path)


def test_discover_mvtec_records_maps_good_to_normal_and_defect_folders_to_anomaly(tmp_path: Path) -> None:
    dataset_root = tmp_path / "mvtec_subset"
    _write_image(dataset_root / "bottle" / "train" / "good" / "normal_1.png", (32, 32, 32))
    _write_image(dataset_root / "bottle" / "train" / "crack" / "defect_1.png", (220, 32, 32))
    _write_image(dataset_root / "cable" / "train" / "good" / "normal_2.jpg", (40, 40, 40))
    _write_image(dataset_root / "cable" / "train" / "cut" / "defect_2.png", (32, 220, 32))

    records = discover_mvtec_records(dataset_root, split="train")

    assert len(records) == 4
    assert sorted(record.label for record in records) == [0, 0, 1, 1]
    assert {record.defect_type for record in records} == {"good", "crack", "cut"}
    assert {record.category for record in records} == {"bottle", "cable"}

    counts = class_counts(records)
    assert counts["normal"] == 2
    assert counts["anomaly"] == 2
    assert counts["defect_types"] == {"good": 2, "crack": 1, "cut": 1}
