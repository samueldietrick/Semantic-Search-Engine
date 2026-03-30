"""Mapeia IDs de negocio para IDs aceitos pelo Qdrant (uint ou UUID)."""

from __future__ import annotations

import uuid
from typing import Any

# Namespace fixo: mesmo ID logico sempre gera o mesmo ponto no Qdrant.
_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/semantic-search-engine/point-id")


def to_qdrant_point_id(raw: Any) -> int | uuid.UUID:
    """
    Qdrant (REST) aceita unsigned integer ou UUID.
    Strings como 'item:1' viram UUID v5 deterministico.
    """
    if isinstance(raw, bool):
        raise ValueError("id booleano invalido")
    if isinstance(raw, int):
        if raw < 0:
            raise ValueError("id inteiro deve ser >= 0")
        return raw
    s = str(raw).strip()
    if not s:
        raise ValueError("id vazio")
    if s.isdigit():
        return int(s)
    return uuid.uuid5(_NAMESPACE, s)
