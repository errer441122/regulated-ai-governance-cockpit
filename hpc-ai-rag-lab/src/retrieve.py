from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

from build_index import Chunk


def _fallback_similarity(query: str, text: str) -> float:
    query_tokens = set(re.findall(r"[a-zA-Z]+", query.lower()))
    text_tokens = set(re.findall(r"[a-zA-Z]+", text.lower()))
    if not query_tokens or not text_tokens:
        return 0.0
    return len(query_tokens & text_tokens) / math.sqrt(len(query_tokens) * len(text_tokens))


def retrieve(query: str, chunks: list[Chunk], top_k: int = 3) -> list[dict[str, Any]]:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
    except ModuleNotFoundError:
        scored = [
            {"chunk_id": chunk.chunk_id, "path": chunk.path, "text": chunk.text, "score": round(_fallback_similarity(query, chunk.text), 4)}
            for chunk in chunks
        ]
    else:
        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform([chunk.text for chunk in chunks] + [query])
        scores = cosine_similarity(matrix[-1], matrix[:-1])[0]
        scored = [
            {"chunk_id": chunk.chunk_id, "path": chunk.path, "text": chunk.text, "score": round(float(score), 4)}
            for chunk, score in zip(chunks, scores)
        ]
    return sorted(scored, key=lambda row: row["score"], reverse=True)[:top_k]


def keyword_summary(chunks: list[Chunk]) -> dict[str, int]:
    tokens = Counter()
    for chunk in chunks:
        tokens.update(re.findall(r"[a-zA-Z]{5,}", chunk.text.lower()))
    return dict(tokens.most_common(8))
