#!/usr/bin/env python3
"""Run integration pytest slice (API + optional PostGIS skipped)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/integration",
        "-q",
        "-m",
        "not postgis",
    ]
    print(" ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
