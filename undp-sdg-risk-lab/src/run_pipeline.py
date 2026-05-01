from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from build_sdg_features import build_features, load_indicator_rows
from text_mining import load_text_rows, topic_keywords
from write_policy_note import write_policy_note, write_responsible_checklist


ARTIFACT_DIR = BASE_DIR / "artifacts"


def write_topics(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["signal_id", "iso3", "topic_keywords", "method"])
        writer.writeheader()
        writer.writerows(rows)


def run(output_dir: Path = ARTIFACT_DIR) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    scored = build_features(load_indicator_rows())
    topics = topic_keywords(load_text_rows())
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows": len(scored),
        "capacity_support_flags": sum(int(row["capacity_support_flag"]) for row in scored),
        "average_sdg_risk_score": round(sum(float(row["sdg_risk_score"]) for row in scored) / len(scored), 4),
        "top_contexts": [row["iso3"] for row in sorted(scored, key=lambda item: float(item["sdg_risk_score"]), reverse=True)[:3]],
        "boundary": "Briefing aid only; no automated aid, eligibility, procurement, targeting, or policy decisions.",
    }
    (output_dir / "sdg_risk_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    write_topics(output_dir / "nlp_topic_summary.csv", topics)
    write_policy_note(output_dir / "sdg_policy_note.md", scored)
    write_responsible_checklist(output_dir / "responsible_data_checklist.md")
    return summary


def main() -> None:
    summary = run()
    print(
        "UNDP SDG risk lab completed: "
        f"rows={summary['rows']} flags={summary['capacity_support_flags']} "
        f"average_score={summary['average_sdg_risk_score']}"
    )


if __name__ == "__main__":
    main()
