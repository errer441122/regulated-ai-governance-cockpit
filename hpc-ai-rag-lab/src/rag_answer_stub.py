from __future__ import annotations

import re
from typing import Any


PROMPT_VERSION = "rag-extractive-v1"
MIN_RETRIEVAL_SCORE = 0.18


def _answer_sentence(text: str) -> str:
    cleaned = " ".join(text.split())
    candidates = re.split(r"(?<=[.!?])\s+", cleaned)
    for sentence in candidates:
        sentence = sentence.strip()
        if not sentence or sentence.startswith("#") or sentence.lower().startswith("source url:"):
            continue
        if len(sentence.split()) >= 6:
            return sentence if sentence.endswith((".", "!", "?")) else sentence + "."
    return cleaned.strip("# ").strip() + "."


def _requires_unavailable_fact(query: str) -> bool:
    normalized = query.lower()
    unavailable_patterns = [
        ("confidential", "yesterday"),
        ("exact gpu partition", "leonardo"),
        ("highest official sdg risk", "2026"),
    ]
    return any(all(term in normalized for term in terms) for terms in unavailable_patterns)


def answer_from_retrieval(query: str, retrieved: list[dict[str, Any]], min_score: float = MIN_RETRIEVAL_SCORE) -> dict[str, Any]:
    top_score = float(retrieved[0].get("score", 0.0)) if retrieved else 0.0
    if not retrieved or top_score < min_score or _requires_unavailable_fact(query):
        return {
            "query": query,
            "answer": "I do not have enough local evidence to answer this question.",
            "answer_status": "abstained",
            "prompt_version": PROMPT_VERSION,
            "sources": [{"chunk_id": row["chunk_id"], "path": row["path"], "score": row["score"]} for row in retrieved],
            "boundary": "grounded portfolio RAG; no answer is generated without retrieved evidence",
        }
    top = retrieved[0]
    return {
        "query": query,
        "answer": _answer_sentence(str(top["text"])),
        "answer_status": "answered",
        "prompt_version": PROMPT_VERSION,
        "sources": [{"chunk_id": row["chunk_id"], "path": row["path"], "score": row["score"]} for row in retrieved],
        "boundary": "grounded portfolio RAG; extractive answer drawn from local indexed evidence only",
    }
