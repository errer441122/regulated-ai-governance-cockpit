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
from grounding import grounding_check
from rag_answer_stub import answer_from_retrieval
from retrieve import retrieve


ARTIFACT_DIR = BASE_DIR / "artifacts"


QUERIES = [
    {"query": "What decisions must not be automated?", "expected_path": "data/sample_governance_docs/ai_policy_note.md", "expected_behavior": "answerable"},
    {"query": "What would a real AI Factory run require for data management?", "expected_path": "data/sample_governance_docs/data_management_note.md", "expected_behavior": "answerable"},
    {"query": "Which risks come from simulated metrics and false precision?", "expected_path": "data/sample_governance_docs/risk_register_note.md", "expected_behavior": "answerable"},
    {"query": "Which controls are needed for trustworthy AI governance?", "expected_path": "data/public_governance_docs/nist_ai_rmf_note.md", "expected_behavior": "answerable"},
    {"query": "What does a high-risk AI system need before deployment?", "expected_path": "data/public_governance_docs/eu_ai_act_note.md", "expected_behavior": "answerable"},
    {"query": "What should a public-sector AI project check about proportionate data use and local context?", "expected_path": "data/public_governance_docs/undp_digital_strategy_note.md", "expected_behavior": "answerable"},
    {"query": "What provenance fields should an SDG analytics workflow record?", "expected_path": "data/public_governance_docs/sdg_indicator_note.md", "expected_behavior": "answerable"},
    {
        "query": "Which confidential Ducati factory asset failed yesterday?",
        "expected_path": None,
        "expected_behavior": "documented_failure",
        "failure_mode": "out_of_scope_confidential_data",
    },
    {
        "query": "What exact GPU partition did this workload use on Leonardo last night?",
        "expected_path": None,
        "expected_behavior": "documented_failure",
        "failure_mode": "missing_execution_evidence",
    },
    {
        "query": "Which country has the highest official SDG risk score in 2026?",
        "expected_path": None,
        "expected_behavior": "documented_failure",
        "failure_mode": "missing_official_country_ranking",
    },
]


def run_benchmark(quick: bool = False, output_dir: Path = ARTIFACT_DIR) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    chunks = load_documents()
    queries = QUERIES[:2] if quick else QUERIES
    started = time.perf_counter()
    results = []
    correct = 0
    grounded_answers = 0
    documented_failures = 0
    hallucination_risk_scores = []
    for query in queries:
        retrieved = retrieve(query["query"], chunks, top_k=3)
        answer = answer_from_retrieval(query["query"], retrieved)
        check = grounding_check(answer["answer"], retrieved, answer_status=str(answer.get("answer_status", "answered")))
        is_correct = bool(
            query["expected_behavior"] == "answerable"
            and retrieved
            and retrieved[0]["path"] == query["expected_path"]
            and answer.get("answer_status") == "answered"
        )
        if is_correct:
            correct += 1
        if check["grounded"]:
            grounded_answers += 1
        if query["expected_behavior"] == "documented_failure" and answer.get("answer_status") == "abstained":
            documented_failures += 1
        hallucination_risk_scores.append(float(check["hallucination_risk_score"]))
        results.append(
            {
                **query,
                "top_result": retrieved[0] if retrieved else None,
                "answer": answer,
                "grounding_check": check,
                "eval_outcome": "correct" if is_correct else "documented_failure",
            }
        )
    elapsed = time.perf_counter() - started
    answerable_questions = sum(1 for query in queries if query["expected_behavior"] == "answerable")
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "documents": len({chunk.path for chunk in chunks}),
        "chunks": len(chunks),
        "queries": len(queries),
        "answerable_questions": answerable_questions,
        "adversarial_questions": len(queries) - answerable_questions,
        "top_k_accuracy": round(correct / len(queries), 4),
        "grounded_answers": grounded_answers,
        "grounding_coverage": round(grounded_answers / len(queries), 4),
        "documented_failures": documented_failures,
        "mean_hallucination_risk_score": round(sum(hallucination_risk_scores) / len(hallucination_risk_scores), 4),
        "total_latency_seconds": round(elapsed, 4),
        "average_query_latency_seconds": round(elapsed / len(queries), 4),
        "hardware_note": platform.platform(),
        "boundary": "local CPU retrieval and grounding benchmark; not executed on a real CINECA/IT4LIA cluster",
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
