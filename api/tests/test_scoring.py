from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
API_DIR = ROOT / "api"
for p in (ROOT, API_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from app.scoring import explain_hybrid, lexical_score_and_signals


def test_lexical_finds_tag_and_title() -> None:
    doc = {
        "id": "item:1",
        "titulo": "Curso de Laravel",
        "descricao": "Backend com PHP",
        "tags": ["php", "backend", "laravel"],
        "metadata": {"categoria": "curso"},
    }
    score, highlights, sig = lexical_score_and_signals(doc, ["laravel", "backend"])
    assert score > 0
    assert "laravel" in highlights or "backend" in highlights


def test_explain_hybrid_returns_reasons() -> None:
    doc = {"metadata": {"categoria": "curso"}}
    reasons = explain_hybrid(0.8, 0.5, ["laravel"], ["Tag relacionada a 'laravel'"], doc)
    assert any("similaridade" in r.lower() for r in reasons)
    assert len(reasons) >= 1
