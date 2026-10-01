"""HISTORICAL_REPLAY backtest CLI: fixture → V1 formulas → hit/miss report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PLATFORM = ROOT / "platform"
if str(PLATFORM) not in sys.path:
    sys.path.insert(0, str(PLATFORM))

from application.flood_assessment import run_flood_slice  # noqa: E402

from adapters.storage.simulated_json import load_fixture  # noqa: E402
from domains.backtesting.metrics import (  # noqa: E402
    DEFAULT_PHI_HIT_THRESHOLD,
    score_units,
)
from domains.common import DATA_CLASS_HISTORICAL_REPLAY, DATA_CLASS_LIVE  # noqa: E402
from harness.backtesting.figure import phi_backtest_svg  # noqa: E402
from hazards.flood.phi import FORMULA_VERSION  # noqa: E402


def load_ground_truth(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("ground truth must be an object")
    return payload


def run_backtest(scenario_path: Path, seed: int) -> dict[str, Any]:
    scenario = yaml.safe_load(scenario_path.read_text(encoding="utf-8"))
    if not isinstance(scenario, dict):
        raise SystemExit("scenario must be a mapping")
    if scenario.get("data_class") == DATA_CLASS_LIVE:
        raise SystemExit("refusing LIVE scenario")
    if scenario.get("data_class") != DATA_CLASS_HISTORICAL_REPLAY:
        raise SystemExit("backtest runner requires data_class=HISTORICAL_REPLAY")
    fixture_id = str(scenario["scenario_id"])
    fixture = load_fixture(fixture_id)
    slice_result = run_flood_slice(fixture, seed=seed)
    truth_rel = scenario.get("ground_truth")
    if not truth_rel:
        raise SystemExit("scenario.ground_truth path is required")
    truth = load_ground_truth(ROOT / str(truth_rel))
    by_unit = {row["spatial_unit_id"]: row for row in truth["units"]}
    rows = []
    for unit in slice_result.units:
        gt = by_unit.get(unit.spatial_unit_id)
        if gt is None:
            raise SystemExit(f"missing ground truth for {unit.spatial_unit_id}")
        rows.append(
            {
                "spatial_unit_id": unit.spatial_unit_id,
                "phi": unit.phi.value,
                "rainfall_mm": unit.observation.value,
                "accumulation": unit.observation.provenance.get("accumulation", "1h"),
                "observed_at": unit.observation.observed_at,
                "ground_truth_flooded": gt["ground_truth_flooded"],
            }
        )
    report = score_units(
        rows,
        scenario_id=fixture_id,
        seed=seed,
        formula_version_phi=FORMULA_VERSION,
        phi_hit_threshold=DEFAULT_PHI_HIT_THRESHOLD,
        limitations=tuple(truth.get("limitations") or ()),
    )
    payload = report.to_dict()
    payload["run_id"] = slice_result.run_id
    payload["data_class"] = slice_result.data_class
    payload["as_of"] = slice_result.as_of
    payload["disclaimer"] = slice_result.disclaimer
    payload["scenario_version"] = scenario.get("version")
    payload["country_iso"] = scenario.get("country_iso")
    payload["site_id"] = scenario.get("site_id")
    payload["time_window"] = scenario.get("time_window")
    payload["ground_truth_type"] = truth.get("ground_truth_type")
    payload["ground_truth_scope"] = truth.get("ground_truth_scope")
    payload["assessments"] = slice_result.to_dict()["assessments"]
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="POLARIS HISTORICAL_REPLAY backtest")
    parser.add_argument(
        "--scenario",
        type=Path,
        default=ROOT / "simulation" / "scenarios" / "flood-mocoa-2017-replay.yaml",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--figure", type=Path, default=None)
    args = parser.parse_args(argv)
    payload = run_backtest(args.scenario, args.seed)
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    if args.figure:
        args.figure.parent.mkdir(parents=True, exist_ok=True)
        args.figure.write_text(phi_backtest_svg(payload), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
