#!/usr/bin/env python3
"""Exercise SIMULATED IoT fault scenarios (gateway down, packet loss)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SCENARIOS = [
    ("iot-bogota-fault-gateway-down.yaml", 42),
    ("iot-bogota-fault-packet-loss.yaml", 0),
]


def main() -> int:
    rc = 0
    for name, seed in SCENARIOS:
        path = f"simulation/scenarios/{name}"
        cmd = [
            sys.executable,
            "-m",
            "simulation.python.iot_run",
            "--scenario",
            path,
            "--seed",
            str(seed),
        ]
        print(" ".join(cmd), flush=True)
        rc |= subprocess.call(cmd, cwd=ROOT)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
