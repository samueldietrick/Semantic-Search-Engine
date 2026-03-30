"""Normalização de texto, stopwords e tokenização para busca lexical."""

from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

# Stopwords PT + EN comuns para busca genérica
_STOPWORDS = frozenset(
    {
        "a",
        "o",
        "os",
        "as",
        "um",
        "uma",
        "uns",
        "umas",
        "de",
        "do",
        "da",
        "dos",
        "das",
        "em",
        "no",
        "na",
        "nos",
        "nas",
        "por",
        "para",
        "com",
        "sem",
        "sobre",
        "que",
        "e",
        "ou",
        "the",
        "a",
        "an",
        "and",
        "or",
        "of",
        "to",
        "in",
        "for",
        "on",
        "with",
        "at",
        "by",
        "from",
        "as",
        "is",
        "was",
        "are",
        "be",
        "this",
        "that",
        "it",
        "quero",
        "uma",
        "uns",
    }
)


def remove_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_text(text: str) -> str:
    if not text:
        return ""
    t = remove_accents(text.lower())
    t = re.sub(r"[^\w\s]", " ", t, flags=re.UNICODE)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def tokenize(text: str, *, use_stopwords: bool = True) -> list[str]:
    n = normalize_text(text)
    if not n:
        return []
    parts = n.split()
    if use_stopwords:
        return [p for p in parts if p not in _STOPWORDS and len(p) > 1]
    return [p for p in parts if len(p) > 1]


@lru_cache(maxsize=4096)
def tokenize_cached(text: str) -> tuple[str, ...]:
    return tuple(tokenize(text))
