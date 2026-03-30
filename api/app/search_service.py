from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

from cachetools import TTLCache
from qdrant_client import QdrantClient

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.text import tokenize

from .config import Settings, get_settings
from .embedder import embed_query
from .models import SearchHit, SearchResponse
from .scoring import explain_hybrid, lexical_score_and_signals

_cache: TTLCache[str, SearchResponse] | None = None


def _get_cache(settings: Settings) -> TTLCache[str, SearchResponse]:
    global _cache
    if _cache is None:
        _cache = TTLCache(maxsize=settings.cache_max_entries, ttl=settings.cache_ttl_seconds)
    return _cache


def _cache_key(q: str, limit: int, offset: int, collection: str) -> str:
    raw = f"{q}|{limit}|{offset}|{collection}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _payload_to_hit(
    doc: dict[str, Any],
    *,
    score: float,
    score_semantic: float,
    score_lexical: float,
    highlights: list[str],
    reasons: list[str],
) -> SearchHit:
    titulo = None
    for k in ("titulo", "title", "nome", "name"):
        v = doc.get(k)
        if isinstance(v, str) and v.strip():
            titulo = v.strip()
            break
    desc = None
    for k in ("descricao", "description", "bio", "resumo"):
        v = doc.get(k)
        if isinstance(v, str) and v.strip():
            desc = v.strip()
            break
    tags: list[str] = []
    t = doc.get("tags")
    if isinstance(t, list):
        tags = [str(x) for x in t if x is not None]
    meta = doc.get("metadata")
    if not isinstance(meta, dict):
        meta = {}
    pid = doc.get("id")
    return SearchHit(
        id=str(pid) if pid is not None else "",
        titulo=titulo,
        score=score,
        score_semantic=score_semantic,
        score_lexical=score_lexical,
        highlights=highlights,
        reasons=reasons,
        metadata=meta,
        descricao=desc,
        tags=tags,
    )


def hybrid_search(
    q: str,
    *,
    limit: int,
    offset: int,
    settings: Settings | None = None,
    client: QdrantClient | None = None,
) -> SearchResponse:
    settings = settings or get_settings()
    if client is None:
        client = QdrantClient(url=settings.qdrant_url)

    if offset == 0 and settings.cache_ttl_seconds > 0:
        ck = _cache_key(q.strip(), limit, offset, settings.collection_name)
        c = _get_cache(settings)
        if ck in c:
            return c[ck]

    query_tokens = tokenize(q)
    vec = embed_query(settings.embedding_model, q.strip())

    prefetch = max(settings.qdrant_prefetch, offset + limit * 5)
    qr = client.query_points(
        collection_name=settings.collection_name,
        query=vec,
        limit=prefetch,
        with_payload=True,
    )
    hits = getattr(qr, "points", None) or []

    ranked: list[tuple[dict[str, Any], float, float, float, list[str], list[str]]] = []
    sem_scores = [float(p.score or 0.0) for p in hits]
    sem_max = max(sem_scores) if sem_scores else 1.0
    if sem_max <= 0:
        sem_max = 1.0

    for p in hits:
        payload = p.payload or {}
        if not isinstance(payload, dict):
            continue
        sem = float(p.score or 0.0) / sem_max
        sem = max(0.0, min(1.0, sem))
        lex, highlights, lex_sig = lexical_score_and_signals(payload, query_tokens)
        final = settings.semantic_weight * sem + settings.lexical_weight * lex
        reasons = explain_hybrid(sem, lex, highlights, lex_sig, payload)
        doc = dict(payload)
        ranked.append((doc, final, sem, lex, highlights, reasons))

    ranked.sort(key=lambda x: x[1], reverse=True)
    total = len(ranked)
    page = ranked[offset : offset + limit]
    results = [
        _payload_to_hit(
            d,
            score=round(f, 4),
            score_semantic=round(sem, 4),
            score_lexical=round(lex, 4),
            highlights=h,
            reasons=r,
        )
        for d, f, sem, lex, h, r in page
    ]

    resp = SearchResponse(total=total, results=results)
    if offset == 0 and settings.cache_ttl_seconds > 0:
        _get_cache(settings)[_cache_key(q.strip(), limit, offset, settings.collection_name)] = resp
    return resp
