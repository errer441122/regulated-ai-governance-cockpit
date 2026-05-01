from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = BASE_DIR / "artifacts"

ROWS = [
    {"iso3": "KEN", "country": "Kenya", "lat": -0.02, "lon": 37.91, "internet_users_pct": 29.5, "gov_effectiveness": -0.3, "disaster_risk": 0.62},
    {"iso3": "GHA", "country": "Ghana", "lat": 7.95, "lon": -1.02, "internet_users_pct": 68.2, "gov_effectiveness": 0.05, "disaster_risk": 0.35},
    {"iso3": "NPL", "country": "Nepal", "lat": 28.39, "lon": 84.12, "internet_users_pct": 38.4, "gov_effectiveness": -0.55, "disaster_risk": 0.71},
    {"iso3": "JOR", "country": "Jordan", "lat": 30.59, "lon": 36.24, "internet_users_pct": 88.0, "gov_effectiveness": 0.11, "disaster_risk": 0.28},
]


def _png(path: Path, width: int, height: int, pixels: list[tuple[int, int, int]]) -> None:
    raw = b"".join(b"\x00" + bytes(channel for pixel in pixels[row * width : (row + 1) * width] for channel in pixel) for row in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    payload = b"\x89PNG\r\n\x1a\n"
    payload += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    payload += chunk(b"IDAT", zlib.compress(raw))
    payload += chunk(b"IEND", b"")
    path.write_bytes(payload)


def _draw_outputs(scored: list[dict[str, object]]) -> None:
    width, height = 420, 220
    pixels = [(245, 247, 250)] * (width * height)
    for x in range(width):
        pixels[30 * width + x] = (35, 74, 118)
        pixels[180 * width + x] = (35, 74, 118)
    for row in scored:
        lon = float(row["lon"])
        lat = float(row["lat"])
        x = int((lon + 20) / 130 * (width - 1))
        y = int((40 - lat) / 55 * (height - 1))
        risk = float(row["sdg_risk_score"])
        color = (196, 65, 45) if risk >= 0.55 else (38, 124, 90)
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                px, py = x + dx, y + dy
                if 0 <= px < width and 0 <= py < height:
                    pixels[py * width + px] = color
    _png(ARTIFACT_DIR / "map_output.png", width, height, pixels)

    dash_pixels = [(250, 250, 248)] * (480 * 260)
    for y in range(40, 220):
        for x in range(50, 430):
            if x in {50, 430} or y in {40, 220}:
                dash_pixels[y * 480 + x] = (30, 60, 95)
    for idx, row in enumerate(scored):
        bar_width = int(float(row["sdg_risk_score"]) * 280)
        y0 = 65 + idx * 38
        for y in range(y0, y0 + 18):
            for x in range(120, 120 + bar_width):
                dash_pixels[y * 480 + x] = (196, 65, 45)
    _png(BASE_DIR / "dashboard_mockup.png", 480, 260, dash_pixels)


def run() -> dict[str, object]:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    scored = []
    for row in ROWS:
        connectivity_gap = 1.0 - (row["internet_users_pct"] / 100.0)
        governance_pressure = max(0.0, 0.5 - row["gov_effectiveness"])
        risk = min(1.0, 0.45 * connectivity_gap + 0.35 * row["disaster_risk"] + 0.20 * governance_pressure)
        scored.append({**row, "sdg_risk_score": round(risk, 4)})
    payload = {
        "rows": len(scored),
        "average_sdg_risk_score": round(sum(float(row["sdg_risk_score"]) for row in scored) / len(scored), 4),
        "top_contexts": [row["iso3"] for row in sorted(scored, key=lambda item: float(item["sdg_risk_score"]), reverse=True)[:2]],
        "boundary": "Public aggregate data briefing aid only; no aid-allocation or eligibility decision.",
    }
    (ARTIFACT_DIR / "sdg_metrics.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    (ARTIFACT_DIR / "policy_note.md").write_text(
        "# SDG Policy Note\n\n"
        f"Average SDG risk score: `{payload['average_sdg_risk_score']}`.\n\n"
        "Use: discussion support for public-data capacity planning.\n\n"
        "Boundary: no automated aid allocation, eligibility, procurement, or country-office decision.\n",
        encoding="utf-8",
    )
    _draw_outputs(scored)
    return payload


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
