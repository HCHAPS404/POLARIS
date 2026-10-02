#!/usr/bin/env python3
"""POLARIS Ola 2 E2E harness — simulation chain → pytest e2e → optional PostGIS.

Runs without Docker by default. Pass ``--postgis`` (or set ``POLARIS_DATABASE_URL``)
after ``make db-up`` + ``make db-migrate`` to exercise the PostGIS repository slice.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FLOOD_SCENARIO = "simulation/scenarios/flood-bogota-demo.yaml"
IOT_SCENARIO = "simulation/scenarios/iot-bogota-demo.yaml"
DEFAULT_SEED = 42


def _run(cmd: list[str]) -> int:
    print(" ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description="POLARIS full-chain E2E harness")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--skip-sim",
        action="store_true",
        help="Skip Digital Testbed runners (pytest e2e only)",
    )
    parser.add_argument(
        "--postgis",
        action="store_true",
        help="Run pytest postgis-marked integration tests (requires POLARIS_DATABASE_URL)",
    )
    args = parser.parse_args()

    if not args.skip_sim:
        rc = _run(
            [
                sys.executable,
                "-m",
                "simulation.python.run",
                "--scenario",
                FLOOD_SCENARIO,
                "--seed",
                str(args.seed),
            ]
        )
        if rc != 0:
            return rc

        rc = _run(
            [
                sys.executable,
                "-m",
                "simulation.python.iot_run",
                "--scenario",
                IOT_SCENARIO,
                "--seed",
                str(args.seed),
            ]
        )
        if rc != 0:
            return rc

    rc = _run([sys.executable, "-m", "pytest", "tests/e2e", "-q"])
    if rc != 0:
        return rc

    rc = _run([sys.executable, "harness/demo/run_demo.py"])
    if rc != 0:
        return rc

    if args.postgis or os.environ.get("POLARIS_DATABASE_URL"):
        rc = _run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/integration",
                "-q",
                "-m",
                "postgis",
            ]
        )
        if rc != 0:
            return rc

    print("E2E harness complete.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
