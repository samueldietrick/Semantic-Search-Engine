"""Testes de busca lexical com consultas variadas (sem Qdrant)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
API_DIR = ROOT / "api"
for p in (ROOT, API_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from app.scoring import lexical_score_and_signals


def _doc() -> dict:
    return {
        "id": "item:x",
        "titulo": "Produto barato com boa avaliação",
        "descricao": "Ideal para quem busca custo-benefício e qualidade.",
        "tags": ["promocao", "hardware"],
        "metadata": {"categoria": "produto", "preco": "barato", "avaliacao": 4.7},
    }


def test_query_produto_barato() -> None:
    score, highlights, _ = lexical_score_and_signals(_doc(), ["produto", "barato", "avaliacao"])
    assert score > 0.1
    assert any(h in highlights for h in ("produto", "barato"))


def test_query_autenticacao_artigo() -> None:
    doc = {
        "titulo": "Autenticação em sistemas distribuídos",
        "descricao": "Tokens stateless e sessões",
        "tags": ["oauth", "jwt"],
        "metadata": {"categoria": "artigo"},
    }
    score, _, _ = lexical_score_and_signals(doc, ["autenticacao", "sistemas"])
    assert score >= 0


def test_query_backend_experiencia() -> None:
    doc = {
        "titulo": "Ana Backend",
        "descricao": "10 anos em microsserviços e APIs",
        "tags": ["java", "backend"],
        "metadata": {"categoria": "usuario"},
    }
    score, highlights, _ = lexical_score_and_signals(doc, ["backend", "experiencia"])
    assert score > 0
    assert "backend" in highlights
