"""Hazard Model Registry — maps hazard_id to config and slice runners.

Evidence: IMPLEMENTED for flood, landslide, and wildfire baselines; other hazards NOT IMPLEMENTED.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]

SliceRunner = Callable[[dict[str, Any], int], Any]


@dataclass(frozen=True)
class HazardRegistryEntry:
    hazard_id: str
    evidence: str
    config_path: Path
    formula_version: str
    model_version: str
    notes: str


_REGISTRY: dict[str, HazardRegistryEntry] = {
    "flood": HazardRegistryEntry(
        hazard_id="flood",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "flood.yaml",
        formula_version="flood.phi.rainfall-threshold.v0.1.0",
        model_version="flood.baseline.v0.1.0",
        notes="Rainfall-threshold PHI; optional rainfall-hydro merge when water_level_m present.",
    ),
    "landslide": HazardRegistryEntry(
        hazard_id="landslide",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "landslide.yaml",
        formula_version="landslide.phi.slope-moisture-rain.v0.1.0",
        model_version="landslide.baseline.v0.1.0",
        notes="Transparent slope + soil moisture susceptibility with rainfall trigger (max merge).",
    ),
    "wildfire": HazardRegistryEntry(
        hazard_id="wildfire",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "wildfire.yaml",
        formula_version="wildfire.phi.fire-weather-pm.v0.1.0",
        model_version="wildfire.baseline.v0.1.0",
        notes="Fire-weather susceptibility with optional PM2.5 detection (max merge).",
    ),
}


def get_registry_entry(hazard_id: str) -> HazardRegistryEntry:
    entry = _REGISTRY.get(hazard_id)
    if entry is None:
        raise KeyError(f"unknown hazard_id {hazard_id!r}")
    return entry


def list_registered_hazards() -> tuple[str, ...]:
    return tuple(sorted(_REGISTRY))


def resolve_hazard_id(fixture: dict[str, Any]) -> str:
    return str(fixture.get("hazard_id") or "flood")


def run_hazard_slice(fixture: dict[str, Any], *, seed: int = 42) -> Any:
    """Dispatch observation → GCI → PHI → risk → DRAFT for a registered hazard."""
    hazard_id = resolve_hazard_id(fixture)
    if hazard_id == "flood":
        from application.flood_assessment import run_flood_slice

        return run_flood_slice(fixture, seed=seed)
    if hazard_id == "landslide":
        from application.landslide_assessment import run_landslide_slice

        return run_landslide_slice(fixture, seed=seed)
    if hazard_id == "wildfire":
        from application.wildfire_assessment import run_wildfire_slice

        return run_wildfire_slice(fixture, seed=seed)
    raise ValueError(f"no slice runner for hazard_id={hazard_id!r}")
