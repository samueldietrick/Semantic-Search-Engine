from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any, TypeVar

import orjson

T = TypeVar("T")


def iter_json_items(path: Path) -> Iterator[dict[str, Any]]:
    """Suporta JSON array ou JSON Lines (.jsonl)."""
    raw = path.read_bytes()
    if path.suffix.lower() == ".jsonl":
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            yield orjson.loads(line)
        return
    data = orjson.loads(raw)
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                yield item
    elif isinstance(data, dict) and "items" in data:
        for item in data["items"]:
            if isinstance(item, dict):
                yield item
    else:
        raise ValueError("JSON deve ser uma lista de objetos ou { 'items': [...] }")


def chunk_iterable(items: Iterator[T], size: int) -> Iterator[list[T]]:
    batch: list[T] = []
    for x in items:
        batch.append(x)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def document_to_embedding_text(doc: dict[str, Any]) -> str:
    """Texto canônico para embedding (campos comuns + metadata serializada)."""
    parts: list[str] = []
    for key in ("titulo", "title", "nome", "name"):
        v = doc.get(key)
        if isinstance(v, str) and v.strip():
            parts.append(v.strip())
            break
    for key in ("descricao", "description", "bio", "resumo"):
        v = doc.get(key)
        if isinstance(v, str) and v.strip():
            parts.append(v.strip())
            break
    tags = doc.get("tags")
    if isinstance(tags, list):
        parts.extend(str(t) for t in tags if t is not None)
    meta = doc.get("metadata")
    if isinstance(meta, dict):
        parts.extend(f"{k} {v}" for k, v in meta.items() if v is not None)
    return " \n ".join(parts) if parts else json.dumps(doc, ensure_ascii=False)
