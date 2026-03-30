from __future__ import annotations

from typing import Any

from rapidfuzz import fuzz

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.text import normalize_text, tokenize


def _get_title(doc: dict[str, Any]) -> str:
    for k in ("titulo", "title", "nome", "name"):
        v = doc.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def _get_description(doc: dict[str, Any]) -> str:
    for k in ("descricao", "description", "bio", "resumo"):
        v = doc.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def _get_tags(doc: dict[str, Any]) -> list[str]:
    t = doc.get("tags")
    if isinstance(t, list):
        return [str(x) for x in t if x is not None]
    return []


def _metadata_str(meta: Any) -> str:
    if isinstance(meta, dict):
        parts = [f"{k} {v}" for k, v in meta.items() if v is not None]
        return " ".join(parts)
    return ""


def build_field_texts(doc: dict[str, Any]) -> dict[str, tuple[str, float]]:
    """Campo → (texto normalizado, peso para boost)."""
    title = normalize_text(_get_title(doc))
    desc = normalize_text(_get_description(doc))
    tags = " ".join(normalize_text(t) for t in _get_tags(doc))
    meta = normalize_text(_metadata_str(doc.get("metadata")))
    return {
        "titulo": (title, 2.0),
        "descricao": (desc, 1.0),
        "tags": (tags, 1.5),
        "metadata": (meta, 0.8),
    }


def lexical_score_and_signals(
    doc: dict[str, Any],
    query_tokens: list[str],
    *,
    fuzzy_threshold: int = 88,
) -> tuple[float, list[str], list[str]]:
    """
    Retorna score lexical [0,1] (aprox.), highlights e sinais para reasons.
    Combina contagem de termos + fuzzy quando não há match exato.
    """
    if not query_tokens:
        return 0.0, [], []

    fields = build_field_texts(doc)
    total_weight = 0.0
    matched_score = 0.0
    highlights: set[str] = set()
    signals: list[str] = []

    for fname, (ftext, boost) in fields.items():
        if not ftext.strip():
            continue
        total_weight += boost * len(query_tokens)
        for qt in query_tokens:
            if not qt:
                continue
            if qt in ftext.split():
                matched_score += boost
                if len(qt) > 2:
                    highlights.add(qt)
                continue
            if qt in ftext:
                matched_score += boost * 0.95
                highlights.add(qt)
                continue
            ratio = fuzz.partial_ratio(qt, ftext)
            if ratio >= fuzzy_threshold:
                matched_score += boost * (ratio / 100.0) * 0.65
                highlights.add(qt)
                if fname == "tags":
                    signals.append(f"Tag relacionada a '{qt}'")
                elif fname == "titulo":
                    signals.append(f"Título alinhado ao termo '{qt}'")

    if total_weight <= 0:
        return 0.0, sorted(highlights), signals

    raw = matched_score / total_weight
    raw = min(1.0, raw)

    merged = " ".join(t for _, (t, _) in fields.items() if t)
    for qt in query_tokens:
        if qt in merged and qt not in highlights and len(qt) > 2:
            highlights.add(qt)

    return raw, sorted(highlights), signals


def explain_hybrid(
    score_semantic: float,
    score_lexical: float,
    highlights: list[str],
    lexical_signals: list[str],
    doc: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []

    if score_semantic >= 0.55:
        reasons.append("Alta similaridade semântica com a busca")
    elif score_semantic >= 0.35:
        reasons.append("Similaridade semântica moderada com a consulta")
    else:
        reasons.append("Correspondência semântica parcial")

    if score_lexical >= 0.4:
        reasons.append("Boa correspondência lexical (título, descrição ou tags)")
    elif score_lexical >= 0.15:
        reasons.append("Alguns termos da busca aparecem no conteúdo")

    meta = doc.get("metadata")
    if isinstance(meta, dict) and meta:
        cat = meta.get("categoria") or meta.get("category")
        if isinstance(cat, str) and cat.strip():
            reasons.append(f"Categoria/metadata: {cat.strip()}")

    for s in lexical_signals[:2]:
        if s not in reasons:
            reasons.append(s)

    for h in highlights[:3]:
        reasons.append(f"Termo relevante '{h}' encontrado")

    return reasons[:6]
