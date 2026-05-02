from __future__ import annotations

import re
from typing import Any


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def grounding_check(answer: str, retrieved: list[dict[str, Any]], answer_status: str = "answered") -> dict[str, Any]:
    normalized_answer = _normalize(answer)
    normalized_sources = [_normalize(str(row.get("text", ""))) for row in retrieved]
    grounded = answer_status == "answered" and bool(normalized_answer) and any(normalized_answer in source for source in normalized_sources)

    unsupported_terms: list[str] = []
    if not grounded:
        source_terms = set(" ".join(normalized_sources).split())
        unsupported_terms = sorted(
            {
                term
                for term in normalized_answer.split()
                if len(term) > 4 and term not in source_terms
            }
        )

    if answer_status == "abstained":
        hallucination_risk_score = 0.65
        risk_reason = "query is outside the local evidence boundary; a forced answer would be high risk"
    elif grounded:
        source_count = max(1, len(retrieved))
        hallucination_risk_score = min(0.3, 0.05 + 0.03 * (source_count - 1))
        risk_reason = "extractive answer is supported by a retrieved chunk; residual risk remains from retrieval choice and source coverage"
    else:
        hallucination_risk_score = 0.85
        risk_reason = "answer text is not fully contained in retrieved evidence"

    return {
        "grounded": grounded,
        "source_count": len(retrieved),
        "unsupported_terms": unsupported_terms[:12],
        "hallucination_risk_score": round(hallucination_risk_score, 4),
        "risk_reason": risk_reason,
    }
