"""CLI harness for SIMULATED IoT vertical slice.

Usage:
  python -m simulation.python.iot_run --scenario simulation/scenarios/iot-bogota-demo.yaml --seed 42
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from simulation.python.iot.pipeline import run_iot_scenario_path  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="POLARIS SIMULATED IoT pipeline runner")
    parser.add_argument(
        "--scenario",
        type=Path,
        default=ROOT / "simulation" / "scenarios" / "iot-bogota-demo.yaml",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)
    payload = run_iot_scenario_path(args.scenario, seed=args.seed)
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
