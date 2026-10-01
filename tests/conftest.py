"""Pytest defaults — in-memory storage unless PostGIS integration marker."""

from __future__ import annotations

import os

os.environ.setdefault("POLARIS_USE_MEMORY_REPO", "1")
