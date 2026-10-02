"""Execute catalogued fault-injection scenarios (harness-only)."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PLATFORM = ROOT / "platform"
if str(PLATFORM) not in sys.path:
    sys.path.insert(0, str(PLATFORM))

from adapters.storage.simulated_json import FixtureNotFoundError, load_fixture  # noqa: E402
from harness.backtesting.replay import run_backtest  # noqa: E402
from simulation.python.energy.node_energy import simulate_cycles  # noqa: E402
from simulation.python.rf.link_budget import free_space_path_loss_db  # noqa: E402

SCENARIOS = Path(__file__).parent / "scenarios.yaml"


def _load_catalog() -> list[dict[str, Any]]:
    raw = yaml.safe_load(SCENARIOS.read_text(encoding="utf-8"))
    return list(raw.get("scenarios") or [])


def _run_scenario(scenario_id: str) -> dict[str, Any]:
    if scenario_id == "missing_ground_truth_unit":
        scenario = ROOT / "simulation/scenarios/flood-mocoa-2017-replay.yaml"
        with tempfile.TemporaryDirectory() as tmp:
            gt_path = Path(tmp) / "bad-gt.json"
            gt_path.write_text(
                json.dumps(
                    {
                        "units": [
                            {
                                "spatial_unit_id": "co-mocoa-2017-acueducto-3h",
                                "ground_truth_flooded": True,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            patched = yaml.safe_load(scenario.read_text(encoding="utf-8"))
            patched["ground_truth"] = str(gt_path)
            patch_file = Path(tmp) / "scenario.yaml"
            patch_file.write_text(yaml.dump(patched), encoding="utf-8")
            try:
                run_backtest(patch_file, 42)
                return {"injected": False, "error": None}
            except SystemExit as exc:
                return {"injected": True, "error": str(exc)}
    if scenario_id == "live_data_class_refused":
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as fh:
            yaml.dump({"data_class": "LIVE", "scenario_id": "x"}, fh)
            path = Path(fh.name)
        try:
            run_backtest(path, 42)
            return {"injected": False, "error": None}
        except SystemExit as exc:
            return {"injected": True, "error": str(exc)}
        finally:
            path.unlink(missing_ok=True)
    if scenario_id == "wrong_replay_data_class":
        try:
            run_backtest(ROOT / "simulation/scenarios/flood-bogota-demo.yaml", 42)
            return {"injected": False, "error": None}
        except SystemExit as exc:
            return {"injected": True, "error": str(exc)}
    if scenario_id == "unknown_fixture":
        try:
            load_fixture("does-not-exist-fixture")
            return {"injected": False, "error": None}
        except FixtureNotFoundError as exc:
            return {"injected": True, "error": str(exc)}
    if scenario_id == "compound_hazard_mismatch":
        from domains.compound.chi_engine import CompoundChiInputs, build_chi_record
        from domains.compound.chi_rules import load_rule

        rule = load_rule("flood-landslide-rain-coupling")
        try:
            build_chi_record(
                spatial_unit_id="u1",
                inputs=CompoundChiInputs(
                    hazard_ids=("wildfire", "landslide"),
                    phi_values=(0.5, 0.5),
                    phi_formula_versions=("a", "b"),
                    rule_id=rule.rule_id,
                ),
                source_ids=("s",),
                observed_at="2026-01-01T00:00:00Z",
                computed_at="2026-01-01T00:01:00Z",
                quality_flags=("qc_pass",),
                data_class="SIMULATED",
                run_id="fault",
                rule=rule,
            )
            return {"injected": False, "error": None}
        except ValueError as exc:
            return {"injected": True, "error": str(exc)}
    if scenario_id == "rf_invalid_frequency":
        try:
            free_space_path_loss_db(distance_m=10.0, frequency_mhz=0.0)
            return {"injected": False, "error": None}
        except ValueError as exc:
            return {"injected": True, "error": str(exc)}
    if scenario_id == "energy_zero_cycles":
        try:
            simulate_cycles(cycles=0)
            return {"injected": False, "error": None}
        except ValueError as exc:
            return {"injected": True, "error": str(exc)}
    raise KeyError(f"unknown fault scenario {scenario_id!r}")


def run_all() -> dict[str, Any]:
    results = []
    for entry in _load_catalog():
        sid = str(entry["id"])
        outcome = _run_scenario(sid)
        results.append(
            {
                "id": sid,
                "description": entry.get("description"),
                "expect": entry.get("expect"),
                "injected": outcome["injected"],
                "error": outcome["error"],
            }
        )
    passed = all(r["injected"] for r in results)
    return {"evidence": "IMPLEMENTED", "passed": passed, "scenarios": results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="POLARIS fault-injection harness")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)
    payload = run_all()
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
