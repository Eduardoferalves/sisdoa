# ruff: noqa: E402
from __future__ import annotations

import os
import sys

# Dynamic PYTHONPATH injection to avoid ModuleNotFoundError on Vercel runtime
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(root_path, "src")
for p in (root_path, src_path):
    if p not in sys.path:
        sys.path.insert(0, p)

from src.sisdoa.api.main import app  # noqa: F401
