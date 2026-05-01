from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
TEXT_PATH = BASE_DIR / "data" / "text_signals_sample.csv"
RISK_TERMS = {"capacity", "connectivity", "climate", "crisis", "privacy", "unemployment", "governance", "monitoring"}


def load_text_rows(path: Path = TEXT_PATH) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _fallback_topics(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        tokens = re.findall(r"[a-zA-Z]+", row["text"].lower())
        counts = Counter(token for token in tokens if token in RISK_TERMS)
        keywords = ";".join(token for token, _ in counts.most_common(4)) or "capacity"
        output.append({"signal_id": row["signal_id"], "iso3": row["iso3"], "topic_keywords": keywords, "method": "keyword_fallback"})
    return output


def topic_keywords(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
    except ModuleNotFoundError:
        return _fallback_topics(rows)

    texts = [row["text"] for row in rows]
    vectorizer = TfidfVectorizer(stop_words="english", max_features=24)
    matrix = vectorizer.fit_transform(texts)
    terms = vectorizer.get_feature_names_out()
    output = []
    for index, row in enumerate(rows):
        scores = matrix[index].toarray()[0]
        ranked = sorted(zip(terms, scores), key=lambda item: item[1], reverse=True)
        keywords = ";".join(term for term, score in ranked[:4] if score > 0)
        output.append({"signal_id": row["signal_id"], "iso3": row["iso3"], "topic_keywords": keywords, "method": "tfidf"})
    return output
