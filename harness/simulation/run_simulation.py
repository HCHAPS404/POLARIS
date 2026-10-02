#!/usr/bin/env python3
"""Run deterministic Digital Testbed scenarios (real Python runner)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="POLARIS simulation harness")
    parser.add_argument(
        "--scenario",
        default="simulation/scenarios/flood-bogota-demo.yaml",
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    cmd = [
        sys.executable,
        "-m",
        "simulation.python.run",
        "--scenario",
        args.scenario,
        "--seed",
        str(args.seed),
    ]
    print(" ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
