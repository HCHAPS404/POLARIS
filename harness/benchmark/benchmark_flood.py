#!/usr/bin/env python3
"""Micro-benchmark: flood slice orchestration (real code, not docs-only)."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "platform"))

from adapters.storage.simulated_json import load_fixture  # noqa: E402
from domains.hazards.registry import run_hazard_slice  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    fixture = load_fixture("flood-bogota-demo")
    start = time.perf_counter()
    for _ in range(args.iterations):
        run_hazard_slice(fixture, seed=args.seed)
    elapsed = time.perf_counter() - start
    per_ms = (elapsed / args.iterations) * 1000.0
    print(
        f"benchmark flood slice: iterations={args.iterations} "
        f"total_s={elapsed:.4f} per_run_ms={per_ms:.3f}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
