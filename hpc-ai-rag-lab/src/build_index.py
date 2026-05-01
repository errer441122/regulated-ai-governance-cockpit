from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DOC_DIR = BASE_DIR / "data" / "sample_governance_docs"


@dataclass
class Chunk:
    chunk_id: str
    path: str
    text: str


def load_documents(doc_dir: Path = DOC_DIR) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(doc_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
        for index, paragraph in enumerate(paragraphs):
            chunks.append(Chunk(chunk_id=f"{path.stem}-{index + 1}", path=path.relative_to(BASE_DIR).as_posix(), text=paragraph))
    if not chunks:
        raise ValueError("No governance documents found for retrieval benchmark.")
    return chunks
