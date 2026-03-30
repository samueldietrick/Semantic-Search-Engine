from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
API_DIR = ROOT / "api"
for p in (ROOT, API_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
