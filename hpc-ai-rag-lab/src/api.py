from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from benchmark import run_benchmark
from build_index import load_documents
from grounding import grounding_check
from rag_answer_stub import answer_from_retrieval
from retrieve import retrieve


try:
    from fastapi import FastAPI
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover - dependency-light tests use plain functions
    FastAPI = None
    BaseModel = object
    Field = None


class RAGQuery(BaseModel):
    query: str
    top_k: int = 3


class RAGEvaluationRequest(BaseModel):
    quick: bool = False


def rag_query_payload(payload: dict[str, Any]) -> dict[str, Any]:
    query = str(payload.get("query", "")).strip()
    top_k = int(payload.get("top_k", 3))
    chunks = load_documents()
    retrieved = retrieve(query, chunks, top_k=max(1, min(top_k, 5)))
    answer = answer_from_retrieval(query, retrieved)
    check = grounding_check(answer["answer"], retrieved, answer_status=str(answer.get("answer_status", "answered")))
    return {
        **answer,
        "retrieved": [
            {
                "chunk_id": row["chunk_id"],
                "path": row["path"],
                "score": row["score"],
            }
            for row in retrieved
        ],
        "grounding_check": check,
    }


def rag_evaluation_payload(payload: dict[str, Any] | None = None, output_dir: Path | None = None) -> dict[str, Any]:
    payload = payload or {}
    return run_benchmark(quick=bool(payload.get("quick", False)), output_dir=output_dir or BASE_DIR / "artifacts")


if FastAPI:
    app = FastAPI(title="Governance RAG Evidence API", version="1.0.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": "local-rag-evidence"}

    @app.post("/rag/query")
    def rag_query(request: RAGQuery) -> dict[str, Any]:
        return rag_query_payload(request.model_dump())

    @app.post("/rag/evaluation")
    def rag_evaluation(request: RAGEvaluationRequest) -> dict[str, Any]:
        return rag_evaluation_payload(request.model_dump())
else:
    app = None
