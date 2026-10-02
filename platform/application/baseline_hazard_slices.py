"""Slice runners for baseline hazard plugins (flash_flood through erosion_subsidence)."""

from __future__ import annotations

from typing import Any, Callable
from uuid import NAMESPACE_URL, uuid5

from application.hazard_slice_runner import assess_with_phi, obs_by_unit
from application.slice_result import BaselineHazardSliceResult, baseline_evidence
from domains.common import DISCLAIMER
from domains.observations.models import Observation
from domains.observations.parse import parse_fixture
from hazards.cyclone.phi import compute_phi as cyclone_phi
from hazards.drought.phi import compute_phi as drought_phi
from hazards.earthquake.phi import compute_phi as earthquake_phi
from hazards.erosion_subsidence.phi import compute_phi as erosion_phi
from hazards.flash_flood.phi import compute_phi as flash_flood_phi
from hazards.heat.phi import compute_phi as heat_phi
from hazards.smoke.phi import compute_phi as smoke_phi
from hazards.tsunami.phi import compute_phi as tsunami_phi
from hazards.volcano.phi import compute_phi as volcano_phi


def _run_id(hazard_id: str, fixture_id: str, seed: int) -> str:
    return str(uuid5(NAMESPACE_URL, f"polaris:{hazard_id}-slice:{fixture_id}:{seed}"))


def _finish(
    *,
    hazard_id: str,
    phi_key: str,
    fixture: dict[str, Any],
    seed: int,
    units: list,
    observations: list[Observation],
) -> BaselineHazardSliceResult:
    fixture_id, as_of, _ = parse_fixture(fixture)
    run_id = _run_id(hazard_id, fixture_id, seed)
    data_class = observations[0].data_class if observations else str(fixture.get("data_class"))
    return BaselineHazardSliceResult(
        hazard_id=hazard_id,
        fixture_id=fixture_id,
        run_id=run_id,
        seed=seed,
        as_of=as_of,
        data_class=str(data_class),
        disclaimer=DISCLAIMER,
        units=tuple(units),
        all_observations=tuple(o.to_dict() for o in observations),
        evidence_block=baseline_evidence(phi_key),
        phi_evidence_key=phi_key,
    )


def _run_single_obs_slice(
    fixture: dict[str, Any],
    *,
    seed: int,
    hazard_id: str,
    phi_key: str,
    observed_property: str,
    build_phi: Callable[..., Any],
    build_kwargs: Callable[[Observation], dict[str, Any]],
) -> BaselineHazardSliceResult:
    fixture_id, as_of, observations = parse_fixture(fixture)
    run_id = _run_id(hazard_id, fixture_id, seed)
    targets = [o for o in observations if o.observed_property == observed_property]
    if not targets:
        raise ValueError(f"{hazard_id} slice requires {observed_property!r} observations")
    units = []
    for obs in targets:
        phi = build_phi(
            **build_kwargs(obs),
            phi_mode=obs.phi_mode,
            spatial_unit_id=obs.spatial_unit_id,
            source_id=obs.source_id,
            observed_at=obs.observed_at,
            computed_at=as_of,
            quality_flag=obs.quality_flag,
            data_class=obs.data_class,
            run_id=run_id,
        )
        units.append(assess_with_phi(primary_obs=obs, phi=phi, run_id=run_id, computed_at=as_of))
    return _finish(
        hazard_id=hazard_id,
        phi_key=phi_key,
        fixture=fixture,
        seed=seed,
        units=units,
        observations=list(observations),
    )


def run_flash_flood_slice(fixture: dict[str, Any], *, seed: int = 42) -> BaselineHazardSliceResult:
    def kwargs(obs: Observation) -> dict[str, Any]:
        acc = str(obs.provenance.get("accumulation") or "1h")
        return {"rainfall_mm": obs.value, "accumulation": acc}

    return _run_single_obs_slice(
        fixture,
        seed=seed,
        hazard_id="flash_flood",
        phi_key="flash_flood_phi",
        observed_property="rainfall_mm",
        build_phi=flash_flood_phi,
        build_kwargs=kwargs,
    )


def run_drought_slice(fixture: dict[str, Any], *, seed: int = 42) -> BaselineHazardSliceResult:
    fixture_id, as_of, observations = parse_fixture(fixture)
    run_id = _run_id("drought", fixture_id, seed)
    by_unit = obs_by_unit(tuple(observations))
    units = []
    for _uid, props in by_unit.items():
        precip = props.get("precipitation_mm_30d")
        moisture = props.get("soil_moisture")
        if precip is None or moisture is None:
            raise ValueError(
                "drought slice requires precipitation_mm_30d and soil_moisture per unit"
            )
        primary = precip
        phi = drought_phi(
            precipitation_mm_30d=precip.value,
            soil_moisture=moisture.value,
            phi_mode=primary.phi_mode,
            spatial_unit_id=primary.spatial_unit_id,
            source_id=primary.source_id,
            observed_at=primary.observed_at,
            computed_at=as_of,
            quality_flag=primary.quality_flag,
            data_class=primary.data_class,
            run_id=run_id,
        )
        units.append(
            assess_with_phi(primary_obs=primary, phi=phi, run_id=run_id, computed_at=as_of)
        )
    return _finish(
        hazard_id="drought",
        phi_key="drought_phi",
        fixture=fixture,
        seed=seed,
        units=units,
        observations=list(observations),
    )


def run_heat_slice(fixture: dict[str, Any], *, seed: int = 42) -> BaselineHazardSliceResult:
    fixture_id, as_of, observations = parse_fixture(fixture)
    run_id = _run_id("heat", fixture_id, seed)
    by_unit = obs_by_unit(tuple(observations))
    units = []
    for _uid, props in by_unit.items():
        temp = props.get("temperature_c")
        if temp is None:
            raise ValueError("heat slice requires temperature_c per unit")
        hi = props.get("heat_index_c")
        phi = heat_phi(
            temperature_c=temp.value,
            heat_index_c=hi.value if hi else None,
            phi_mode=temp.phi_mode,
            spatial_unit_id=temp.spatial_unit_id,
            source_id=temp.source_id,
            observed_at=temp.observed_at,
            computed_at=as_of,
            quality_flag=temp.quality_flag,
            data_class=temp.data_class,
            run_id=run_id,
        )
        units.append(assess_with_phi(primary_obs=temp, phi=phi, run_id=run_id, computed_at=as_of))
    return _finish(
        hazard_id="heat",
        phi_key="heat_phi",
        fixture=fixture,
        seed=seed,
        units=units,
        observations=list(observations),
    )


def run_cyclone_slice(fixture: dict[str, Any], *, seed: int = 42) -> BaselineHazardSliceResult:
    fixture_id, as_of, observations = parse_fixture(fixture)
    run_id = _run_id("cyclone", fixture_id, seed)
    by_unit = obs_by_unit(tuple(observations))
    units = []
    for _uid, props in by_unit.items():
        wind = props.get("wind_speed_ms")
        if wind is None:
            raise ValueError("cyclone slice requires wind_speed_ms per unit")
        pres = props.get("pressure_hpa")
        phi = cyclone_phi(
            wind_speed_ms=wind.value,
            pressure_hpa=pres.value if pres else None,
            phi_mode=wind.phi_mode,
            spatial_unit_id=wind.spatial_unit_id,
            source_id=wind.source_id,
            observed_at=wind.observed_at,
            computed_at=as_of,
            quality_flag=wind.quality_flag,
            data_class=wind.data_class,
            run_id=run_id,
        )
        units.append(assess_with_phi(primary_obs=wind, phi=phi, run_id=run_id, computed_at=as_of))
    return _finish(
        hazard_id="cyclone",
        phi_key="cyclone_phi",
        fixture=fixture,
        seed=seed,
        units=units,
        observations=list(observations),
    )


def run_smoke_slice(fixture: dict[str, Any], *, seed: int = 42) -> BaselineHazardSliceResult:
    fixture_id, as_of, observations = parse_fixture(fixture)
    run_id = _run_id("smoke", fixture_id, seed)
    by_unit = obs_by_unit(tuple(observations))
    units = []
    for _uid, props in by_unit.items():
        pm = props.get("pm25_ugm3")
        if pm is None:
            raise ValueError("smoke slice requires pm25_ugm3 per unit")
        vis = props.get("visibility_m")
        phi = smoke_phi(
            pm25_ugm3=pm.value,
            visibility_m=vis.value if vis else None,
            phi_mode=pm.phi_mode,
            spatial_unit_id=pm.spatial_unit_id,
            source_id=pm.source_id,
            observed_at=pm.observed_at,
            computed_at=as_of,
            quality_flag=pm.quality_flag,
            data_class=pm.data_class,
            run_id=run_id,
        )
        units.append(assess_with_phi(primary_obs=pm, phi=phi, run_id=run_id, computed_at=as_of))
    return _finish(
        hazard_id="smoke",
        phi_key="smoke_phi",
        fixture=fixture,
        seed=seed,
        units=units,
        observations=list(observations),
    )


def run_earthquake_slice(fixture: dict[str, Any], *, seed: int = 42) -> BaselineHazardSliceResult:
    return _run_single_obs_slice(
        fixture,
        seed=seed,
        hazard_id="earthquake",
        phi_key="earthquake_phi",
        observed_property="pga_g",
        build_phi=earthquake_phi,
        build_kwargs=lambda obs: {"pga_g": obs.value},
    )


def run_tsunami_slice(fixture: dict[str, Any], *, seed: int = 42) -> BaselineHazardSliceResult:
    fixture_id, as_of, observations = parse_fixture(fixture)
    run_id = _run_id("tsunami", fixture_id, seed)
    by_unit = obs_by_unit(tuple(observations))
    units = []
    for _uid, props in by_unit.items():
        wave = props.get("wave_height_m")
        dist = props.get("distance_km")
        trigger_obs = props.get("tsunami_trigger")
        primary = wave or dist or trigger_obs
        if primary is None:
            raise ValueError(
                "tsunami slice requires wave_height_m, distance_km, or tsunami_trigger"
            )
        prov = primary.provenance
        event_triggered = bool(
            prov.get("event_triggered") or prov.get("trigger_event_id")
        )
        if trigger_obs is not None:
            event_triggered = event_triggered or trigger_obs.value >= 1.0
        phi = tsunami_phi(
            event_triggered=event_triggered,
            wave_height_m=wave.value if wave else None,
            distance_km=dist.value if dist else None,
            trigger_event_id=str(prov.get("trigger_event_id") or "") or None,
            phi_mode=primary.phi_mode,
            spatial_unit_id=primary.spatial_unit_id,
            source_id=primary.source_id,
            observed_at=primary.observed_at,
            computed_at=as_of,
            quality_flag=primary.quality_flag,
            data_class=primary.data_class,
            run_id=run_id,
        )
        units.append(
            assess_with_phi(primary_obs=primary, phi=phi, run_id=run_id, computed_at=as_of)
        )
    return _finish(
        hazard_id="tsunami",
        phi_key="tsunami_phi",
        fixture=fixture,
        seed=seed,
        units=units,
        observations=list(observations),
    )


def run_volcano_slice(fixture: dict[str, Any], *, seed: int = 42) -> BaselineHazardSliceResult:
    fixture_id, as_of, observations = parse_fixture(fixture)
    run_id = _run_id("volcano", fixture_id, seed)
    by_unit = obs_by_unit(tuple(observations))
    units = []
    for _uid, props in by_unit.items():
        so2 = props.get("so2_ton_per_day")
        if so2 is None:
            raise ValueError("volcano slice requires so2_ton_per_day per unit")
        ash = props.get("ashfall_mm_h")
        phi = volcano_phi(
            so2_ton_per_day=so2.value,
            ashfall_mm_h=ash.value if ash else None,
            phi_mode=so2.phi_mode,
            spatial_unit_id=so2.spatial_unit_id,
            source_id=so2.source_id,
            observed_at=so2.observed_at,
            computed_at=as_of,
            quality_flag=so2.quality_flag,
            data_class=so2.data_class,
            run_id=run_id,
        )
        units.append(assess_with_phi(primary_obs=so2, phi=phi, run_id=run_id, computed_at=as_of))
    return _finish(
        hazard_id="volcano",
        phi_key="volcano_phi",
        fixture=fixture,
        seed=seed,
        units=units,
        observations=list(observations),
    )


def run_erosion_subsidence_slice(
    fixture: dict[str, Any], *, seed: int = 42
) -> BaselineHazardSliceResult:
    fixture_id, as_of, observations = parse_fixture(fixture)
    run_id = _run_id("erosion_subsidence", fixture_id, seed)
    by_unit = obs_by_unit(tuple(observations))
    units = []
    for _uid, props in by_unit.items():
        cohesion = props.get("soil_cohesion_proxy")
        slope = props.get("slope_deg")
        rain = props.get("rainfall_mm")
        if cohesion is None or slope is None or rain is None:
            raise ValueError(
                "erosion_subsidence slice requires soil_cohesion_proxy, slope_deg, rainfall_mm"
            )
        primary = slope
        acc = str(rain.provenance.get("accumulation") or "1h")
        phi = erosion_phi(
            soil_cohesion_proxy=cohesion.value,
            slope_deg=slope.value,
            rainfall_mm=rain.value,
            phi_mode=primary.phi_mode,
            spatial_unit_id=primary.spatial_unit_id,
            source_id=primary.source_id,
            observed_at=primary.observed_at,
            computed_at=as_of,
            quality_flag=primary.quality_flag,
            data_class=primary.data_class,
            run_id=run_id,
            accumulation=acc,
        )
        units.append(
            assess_with_phi(primary_obs=primary, phi=phi, run_id=run_id, computed_at=as_of)
        )
    return _finish(
        hazard_id="erosion_subsidence",
        phi_key="erosion_subsidence_phi",
        fixture=fixture,
        seed=seed,
        units=units,
        observations=list(observations),
    )
