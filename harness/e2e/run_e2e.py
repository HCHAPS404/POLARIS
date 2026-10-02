#!/usr/bin/env python3
"""Run e2e pytest package (fixture → API JSON)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    cmd = [sys.executable, "-m", "pytest", "tests/e2e", "-q"]
    print(" ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
