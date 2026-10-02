"""Hazard Model Registry — maps hazard_id to config and slice runners.

Evidence: IMPLEMENTED baselines for all registered hazard plugins in-tree.
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
    phi_mode_policy: str


_REGISTRY: dict[str, HazardRegistryEntry] = {
    "flood": HazardRegistryEntry(
        hazard_id="flood",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "flood.yaml",
        formula_version="flood.phi.rainfall-threshold.v0.1.0",
        model_version="flood.baseline.v0.1.0",
        phi_mode_policy="declared_on_observation",
        notes="Rainfall-threshold PHI; optional rainfall-hydro merge when water_level_m present.",
    ),
    "flash_flood": HazardRegistryEntry(
        hazard_id="flash_flood",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "flash_flood.yaml",
        formula_version="flash_flood.phi.rain-burst.v0.1.0",
        model_version="flash_flood.baseline.v0.1.0",
        phi_mode_policy="declared_on_observation",
        notes="Intense short-window rain burst screening (steeper thresholds than riverine flood).",
    ),
    "landslide": HazardRegistryEntry(
        hazard_id="landslide",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "landslide.yaml",
        formula_version="landslide.phi.slope-moisture-rain.v0.1.0",
        model_version="landslide.baseline.v0.1.0",
        phi_mode_policy="declared_on_observation",
        notes="Transparent slope + soil moisture susceptibility with rainfall trigger (max merge).",
    ),
    "wildfire": HazardRegistryEntry(
        hazard_id="wildfire",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "wildfire.yaml",
        formula_version="wildfire.phi.fire-weather-pm.v0.1.0",
        model_version="wildfire.baseline.v0.1.0",
        phi_mode_policy="declared_on_observation",
        notes="Fire-weather susceptibility with optional PM2.5 detection (max merge).",
    ),
    "drought": HazardRegistryEntry(
        hazard_id="drought",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "drought.yaml",
        formula_version="drought.phi.precip-moisture.v0.1.0",
        model_version="drought.baseline.v0.1.0",
        phi_mode_policy="declared_on_observation",
        notes="30d precipitation deficit + dry soil moisture (max merge).",
    ),
    "heat": HazardRegistryEntry(
        hazard_id="heat",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "heat.yaml",
        formula_version="heat.phi.heat-stress.v0.1.0",
        model_version="heat.baseline.v0.1.0",
        phi_mode_policy="declared_on_observation",
        notes="Air temperature + optional heat-index stress screening.",
    ),
    "cyclone": HazardRegistryEntry(
        hazard_id="cyclone",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "cyclone.yaml",
        formula_version="cyclone.phi.wind-pressure.v0.1.0",
        model_version="cyclone.baseline.v0.1.0",
        phi_mode_policy="declared_on_observation",
        notes="Sustained wind + optional central pressure deficit.",
    ),
    "smoke": HazardRegistryEntry(
        hazard_id="smoke",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "smoke.yaml",
        formula_version="smoke.phi.pm-visibility.v0.1.0",
        model_version="smoke.baseline.v0.1.0",
        phi_mode_policy="declared_on_observation",
        notes="PM2.5 + optional visibility for smoke/air-quality screening.",
    ),
    "earthquake": HazardRegistryEntry(
        hazard_id="earthquake",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "earthquake.yaml",
        formula_version="earthquake.phi.pga-shaking.v0.1.0",
        model_version="earthquake.baseline.v0.1.0",
        phi_mode_policy="rapid_detection_eew_only",
        notes="Observed PGA shaking for RAPID_DETECTION/EEW only — no prediction.",
    ),
    "tsunami": HazardRegistryEntry(
        hazard_id="tsunami",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "tsunami.yaml",
        formula_version="tsunami.phi.event-wave.v0.1.0",
        model_version="tsunami.baseline.v0.1.0",
        phi_mode_policy="event_triggered_only",
        notes="Coastal wave/run-up screening only when a trigger is declared.",
    ),
    "volcano": HazardRegistryEntry(
        hazard_id="volcano",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "volcano.yaml",
        formula_version="volcano.phi.so2-ash.v0.1.0",
        model_version="volcano.baseline.v0.1.0",
        phi_mode_policy="declared_on_observation",
        notes="SO2 emission rate + optional ashfall rate screening.",
    ),
    "erosion_subsidence": HazardRegistryEntry(
        hazard_id="erosion_subsidence",
        evidence="IMPLEMENTED",
        config_path=ROOT / "configs" / "hazards" / "erosion_subsidence.yaml",
        formula_version="erosion_subsidence.phi.cohesion-slope-rain.v0.1.0",
        model_version="erosion_subsidence.baseline.v0.1.0",
        phi_mode_policy="declared_on_observation",
        notes="Weak-soil + slope susceptibility with rainfall trigger.",
    ),
}


def get_registry_entry(hazard_id: str) -> HazardRegistryEntry:
    entry = _REGISTRY.get(hazard_id)
    if entry is None:
        raise KeyError(f"unknown hazard_id {hazard_id!r}")
    return entry


def list_registered_hazards() -> tuple[str, ...]:
    """Hazard IDs with an IMPLEMENTED slice runner."""
    return tuple(sorted(h for h, e in _REGISTRY.items() if e.evidence == "IMPLEMENTED"))


def list_registry_hazard_ids() -> tuple[str, ...]:
    """All hazard IDs known to the registry."""
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
    runners: dict[str, SliceRunner] = {
        "flash_flood": _flash_flood,
        "drought": _drought,
        "heat": _heat,
        "cyclone": _cyclone,
        "smoke": _smoke,
        "earthquake": _earthquake,
        "tsunami": _tsunami,
        "volcano": _volcano,
        "erosion_subsidence": _erosion,
    }
    runner = runners.get(hazard_id)
    if runner is None:
        raise ValueError(f"no slice runner for hazard_id={hazard_id!r}")
    return runner(fixture, seed)


def _flash_flood(fixture: dict[str, Any], seed: int) -> Any:
    from application.baseline_hazard_slices import run_flash_flood_slice

    return run_flash_flood_slice(fixture, seed=seed)


def _drought(fixture: dict[str, Any], seed: int) -> Any:
    from application.baseline_hazard_slices import run_drought_slice

    return run_drought_slice(fixture, seed=seed)


def _heat(fixture: dict[str, Any], seed: int) -> Any:
    from application.baseline_hazard_slices import run_heat_slice

    return run_heat_slice(fixture, seed=seed)


def _cyclone(fixture: dict[str, Any], seed: int) -> Any:
    from application.baseline_hazard_slices import run_cyclone_slice

    return run_cyclone_slice(fixture, seed=seed)


def _smoke(fixture: dict[str, Any], seed: int) -> Any:
    from application.baseline_hazard_slices import run_smoke_slice

    return run_smoke_slice(fixture, seed=seed)


def _earthquake(fixture: dict[str, Any], seed: int) -> Any:
    from application.baseline_hazard_slices import run_earthquake_slice

    return run_earthquake_slice(fixture, seed=seed)


def _tsunami(fixture: dict[str, Any], seed: int) -> Any:
    from application.baseline_hazard_slices import run_tsunami_slice

    return run_tsunami_slice(fixture, seed=seed)


def _volcano(fixture: dict[str, Any], seed: int) -> Any:
    from application.baseline_hazard_slices import run_volcano_slice

    return run_volcano_slice(fixture, seed=seed)


def _erosion(fixture: dict[str, Any], seed: int) -> Any:
    from application.baseline_hazard_slices import run_erosion_subsidence_slice

    return run_erosion_subsidence_slice(fixture, seed=seed)
