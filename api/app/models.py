from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    q: str = Field(..., min_length=1, description="Consulta em linguagem natural")
    limit: int = Field(10, ge=1, le=50)
    offset: int = Field(0, ge=0)


class SearchHit(BaseModel):
    id: str
    titulo: str | None = None
    score: float
    score_semantic: float
    score_lexical: float
    highlights: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    descricao: str | None = None
    tags: list[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    total: int
    results: list[SearchHit]
