"""Ingest SIMULATED IoT scenario through gateway + flood slice."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from simulation.python.iot.pipeline import load_scenario, run_iot_scenario

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCENARIO = ROOT / "simulation" / "scenarios" / "iot-bogota-demo.yaml"


def ingest_iot_scenario(
    *,
    scenario_path: Path | None = None,
    scenario_id: str | None = None,
    seed: int = 42,
) -> dict[str, Any]:
    if scenario_path is None:
        sid = scenario_id or "iot-bogota-demo"
        scenario_path = ROOT / "simulation" / "scenarios" / f"{sid}.yaml"
    if not scenario_path.is_file():
        raise FileNotFoundError(f"IoT scenario not found: {scenario_path}")
    scenario = load_scenario(scenario_path)
    return run_iot_scenario(scenario, seed=seed)
