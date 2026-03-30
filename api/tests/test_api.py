from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent.parent
API_DIR = ROOT / "api"
for p in (ROOT, API_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_search_validation(client: TestClient) -> None:
    r = client.post("/search", json={"q": ""})
    assert r.status_code == 422


@patch("app.main.hybrid_search")
def test_search_returns_results(mock_hybrid: MagicMock, client: TestClient) -> None:
    from app.models import SearchHit, SearchResponse

    mock_hybrid.return_value = SearchResponse(
        total=1,
        results=[
            SearchHit(
                id="item:1",
                titulo="Teste",
                score=0.9,
                score_semantic=0.8,
                score_lexical=0.2,
                highlights=["teste"],
                reasons=["Alta similaridade semântica com a busca"],
                metadata={},
                descricao="desc",
                tags=["a"],
            )
        ],
    )
    r = client.post("/search", json={"q": "produto barato", "limit": 5})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert body["results"][0]["id"] == "item:1"
    assert "score_semantic" in body["results"][0]
