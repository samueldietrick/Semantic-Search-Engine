from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import SearchRequest, SearchResponse
from .search_service import hybrid_search

app = FastAPI(
    title="Semantic Search Engine",
    version="1.0.0",
    description="Busca híbrida (semântica + lexical) com explicabilidade.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest) -> SearchResponse:
    return hybrid_search(req.q.strip(), limit=req.limit, offset=req.offset)
