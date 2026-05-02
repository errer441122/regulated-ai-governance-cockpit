from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from api import rag_evaluation_payload, rag_query_payload  # noqa: E402
from benchmark import QUERIES, run_benchmark  # noqa: E402
from build_index import load_documents  # noqa: E402
from grounding import grounding_check  # noqa: E402
from rag_answer_stub import answer_from_retrieval  # noqa: E402
from retrieve import retrieve  # noqa: E402


def test_rag_evaluation_set_has_answerable_and_adversarial_questions():
    assert len(QUERIES) == 10
    assert len({row["query"] for row in QUERIES}) == 10
    assert sum(1 for row in QUERIES if row["expected_behavior"] == "answerable") == 7
    assert sum(1 for row in QUERIES if row["expected_behavior"] == "documented_failure") == 3


def test_grounding_check_marks_extractive_answer_supported():
    chunks = load_documents()
    retrieved = retrieve("Which controls are needed for trustworthy AI governance?", chunks, top_k=3)
    answer = answer_from_retrieval("Which controls are needed for trustworthy AI governance?", retrieved)
    check = grounding_check(answer["answer"], retrieved)

    assert check["grounded"] is True
    assert check["source_count"] >= 1
    assert check["unsupported_terms"] == []


def test_rag_api_payload_exposes_prompt_version_sources_and_grounding():
    response = rag_query_payload({"query": "What does a high-risk AI system need before deployment?", "top_k": 3})

    assert response["prompt_version"] == "rag-extractive-v1"
    assert response["sources"]
    assert response["grounding_check"]["grounded"] is True
    assert 0.0 < response["grounding_check"]["hallucination_risk_score"] < 1.0
    assert response["boundary"].startswith("grounded portfolio RAG")


def test_rag_api_abstains_for_out_of_scope_question():
    response = rag_query_payload({"query": "Which confidential Ducati factory asset failed yesterday?", "top_k": 3})

    assert response["answer_status"] == "abstained"
    assert response["grounding_check"]["grounded"] is False
    assert response["grounding_check"]["hallucination_risk_score"] >= 0.5


def test_rag_evaluation_payload_reports_grounding_coverage(tmp_path):
    payload = run_benchmark(quick=False, output_dir=tmp_path)
    api_payload = rag_evaluation_payload({"quick": False}, output_dir=tmp_path)

    assert payload["queries"] == 10
    assert payload["answerable_questions"] == 7
    assert payload["documented_failures"] == 3
    assert payload["top_k_accuracy"] == 0.7
    assert payload["grounding_coverage"] == 0.7
    assert api_payload["mean_hallucination_risk_score"] > 0
    assert (tmp_path / "retrieval_benchmark.json").exists()
