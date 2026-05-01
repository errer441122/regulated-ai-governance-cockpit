from __future__ import annotations

from typing import Any


def answer_from_retrieval(query: str, retrieved: list[dict[str, Any]]) -> dict[str, Any]:
    if not retrieved:
        return {
            "query": query,
            "answer": "No local evidence was retrieved.",
            "sources": [],
            "boundary": "extractive local stub; no generative claims",
        }
    top = retrieved[0]
    sentence = str(top["text"]).split(".")[0].strip()
    return {
        "query": query,
        "answer": sentence + ".",
        "sources": [{"chunk_id": top["chunk_id"], "path": top["path"], "score": top["score"]}],
        "boundary": "extractive local stub; answer is drawn from retrieved text only",
    }
