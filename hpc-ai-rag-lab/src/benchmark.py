from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from build_index import load_documents
from rag_answer_stub import answer_from_retrieval
from retrieve import retrieve


ARTIFACT_DIR = BASE_DIR / "artifacts"


QUERIES = [
    {"query": "What decisions must not be automated?", "expected_path": "data/sample_governance_docs/ai_policy_note.md"},
    {"query": "What would a real AI Factory run require for data management?", "expected_path": "data/sample_governance_docs/data_management_note.md"},
    {"query": "Which risks come from simulated metrics and false precision?", "expected_path": "data/sample_governance_docs/risk_register_note.md"},
]


def run_benchmark(quick: bool = False, output_dir: Path = ARTIFACT_DIR) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    chunks = load_documents()
    queries = QUERIES[:2] if quick else QUERIES
    started = time.perf_counter()
    results = []
    correct = 0
    for query in queries:
        retrieved = retrieve(query["query"], chunks, top_k=3)
        answer = answer_from_retrieval(query["query"], retrieved)
        if retrieved and retrieved[0]["path"] == query["expected_path"]:
            correct += 1
        results.append({**query, "top_result": retrieved[0] if retrieved else None, "answer": answer})
    elapsed = time.perf_counter() - started
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "documents": len({chunk.path for chunk in chunks}),
        "chunks": len(chunks),
        "queries": len(queries),
        "top_k_accuracy": round(correct / len(queries), 4),
        "total_latency_seconds": round(elapsed, 4),
        "average_query_latency_seconds": round(elapsed / len(queries), 4),
        "hardware_note": platform.platform(),
        "boundary": "local CPU retrieval benchmark; not executed on a real CINECA/IT4LIA cluster",
        "results": results,
    }
    (output_dir / "retrieval_benchmark.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "sample_queries.json").write_text(json.dumps(queries, indent=2, sort_keys=True), encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    payload = run_benchmark(quick=args.quick)
    print(
        "HPC/RAG benchmark completed: "
        f"documents={payload['documents']} chunks={payload['chunks']} "
        f"queries={payload['queries']} top_k_accuracy={payload['top_k_accuracy']}"
    )


if __name__ == "__main__":
    main()
