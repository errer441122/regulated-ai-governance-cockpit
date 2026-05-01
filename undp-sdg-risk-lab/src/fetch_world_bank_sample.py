from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
FALLBACK_PATH = BASE_DIR / "data" / "public_development_sample.csv"


def get_offline_fallback() -> Path:
    """Return the committed fallback sample.

    A real refresh can be added later, but the lab remains offline-first for
    reproducible reviewer and CI runs.
    """
    return FALLBACK_PATH
