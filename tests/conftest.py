"""Pytest defaults — in-memory storage unless PostGIS integration marker."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLATFORM = ROOT / "platform"
for path in (str(ROOT), str(PLATFORM)):
    if path not in sys.path:
        sys.path.insert(0, path)

os.environ.setdefault("POLARIS_USE_MEMORY_REPO", "1")
