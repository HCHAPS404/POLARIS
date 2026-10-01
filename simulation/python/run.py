"""Deterministic flood slice runner (SIMULATED or HISTORICAL_REPLAY).

Usage:
  python -m simulation.python.run --scenario simulation/scenarios/flood-bogota-demo.yaml --seed 42
  python -m simulation.python.run --scenario simulation/scenarios/flood-mocoa-2017-replay.yaml \\
      --seed 42
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

from domains.common import ALLOWED_DATA_CLASSES, DATA_CLASS_LIVE

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PLATFORM = ROOT / "platform"
if str(PLATFORM) not in sys.path:
    sys.path.insert(0, str(PLATFORM))

from application.flood_assessment import run_flood_slice  # noqa: E402

from adapters.storage.simulated_json import load_fixture  # noqa: E402


def load_scenario(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("scenario must be a mapping")
    data_class = payload.get("data_class")
    if data_class == DATA_CLASS_LIVE:
        raise SystemExit("refusing scenario that is data_class=LIVE")
    if data_class not in ALLOWED_DATA_CLASSES:
        raise SystemExit("refusing scenario that is not SIMULATED or HISTORICAL_REPLAY")
    return payload


def run(scenario_path: Path, seed: int) -> dict[str, Any]:
    scenario = load_scenario(scenario_path)
    fixture_id = str(scenario.get("scenario_id") or scenario.get("fixture") or "")
    fixture = load_fixture(fixture_id)
    result = run_flood_slice(fixture, seed=seed)
    payload = result.to_dict()
    payload["scenario_id"] = scenario.get("scenario_id")
    payload["scenario_seed"] = seed
    payload["scenario_version"] = scenario.get("version")
    payload["country_iso"] = scenario.get("country_iso")
    payload["site_id"] = scenario.get("site_id")
    payload["time_window"] = scenario.get("time_window")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="POLARIS flood slice runner")
    parser.add_argument(
        "--scenario",
        type=Path,
        default=ROOT / "simulation" / "scenarios" / "flood-bogota-demo.yaml",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)
    payload = run(args.scenario, args.seed)
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
