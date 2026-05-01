from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlopen


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OPENML_METADATA_URL = "https://api.openml.org/api/v1/json/data/46929"
OPENML_ARFF_URL = "https://openml.org/data/v1/download/22125240/GiveMeSomeCredit.arff"
RAW_DATA_PATH = DATA_DIR / "GiveMeSomeCredit_openml_46929.arff"
METADATA_PATH = DATA_DIR / "openml_46929_metadata.json"


def fetch_json(url: str) -> dict[str, object]:
    with urlopen(url, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def download_file(url: str, output_path: Path) -> None:
    with urlopen(url, timeout=120) as response, output_path.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)


def fetch() -> dict[str, object]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    metadata = fetch_json(OPENML_METADATA_URL)
    METADATA_PATH.write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    if not RAW_DATA_PATH.exists():
        download_file(OPENML_ARFF_URL, RAW_DATA_PATH)
    return {
        "dataset": "OpenML GiveMeSomeCredit",
        "openml_id": 46929,
        "raw_data_path": str(RAW_DATA_PATH),
        "metadata_path": str(METADATA_PATH),
        "bytes": RAW_DATA_PATH.stat().st_size,
    }


def main() -> None:
    print(json.dumps(fetch(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
