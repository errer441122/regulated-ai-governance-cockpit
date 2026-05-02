from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from benchmark import run_benchmark
from build_index import load_documents
from rag_answer_stub import answer_from_retrieval
from retrieve import retrieve


def test_retrieval_returns_relevant_chunk():
    chunks = load_documents()
    results = retrieve("automated credit and eligibility decisions", chunks, top_k=1)
    assert results
    assert "ai_policy_note" in results[0]["chunk_id"]


def test_document_loader_skips_heading_only_chunks():
    chunks = load_documents()
    assert chunks
    assert all(not chunk.text.startswith("#") for chunk in chunks)
    assert all(not chunk.text.lower().startswith("source url:") for chunk in chunks)


def test_answer_stub_is_extractive():
    chunks = load_documents()
    results = retrieve("data management access controls", chunks, top_k=1)
    answer = answer_from_retrieval("data management access controls", results)
    assert answer["sources"]
    assert "extractive" in answer["boundary"]


def test_benchmark_writes_artifact(tmp_path):
    payload = run_benchmark(quick=True, output_dir=tmp_path)
    assert payload["queries"] == 2
    assert payload["top_k_accuracy"] >= 0.5
    assert (tmp_path / "retrieval_benchmark.json").exists()
    assert (tmp_path / "sample_queries.json").exists()
