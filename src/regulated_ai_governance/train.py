from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TRAIN_SCRIPT = ROOT / "ml-baseline" / "train_model.py"


def _load_train_module():
    spec = importlib.util.spec_from_file_location("regulated_ml_baseline_train_model", TRAIN_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {TRAIN_SCRIPT}.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def train() -> dict[str, Any]:
    module = _load_train_module()
    return module.train()


def main() -> None:
    result = train()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
