from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def _model(name: str) -> SentenceTransformer:
    return SentenceTransformer(name)


def embed_query(model_name: str, text: str) -> list[float]:
    m = _model(model_name)
    v = m.encode([text], convert_to_numpy=True, normalize_embeddings=True)[0]
    return v.tolist()
