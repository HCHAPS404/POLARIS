"""Landslide slice: observation → GCI → PHI → operational risk → DRAFT alert."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from application.flood_assessment import UnitAssessment
from domains.alerting.draft import build_draft_alert
from domains.common import DISCLAIMER
from domains.observations.models import Observation
from domains.observations.parse import parse_fixture
from domains.quality.gci import compute_gci
from domains.risk.operational import compute_operational_risk
from domains.sites.ev_config import (
    ev_config_version_for_site,
    resolve_exposure,
    resolve_vulnerability,
)
from hazards.landslide.phi import compute_phi


@dataclass(frozen=True)
class LandslideSliceResult:
    fixture_id: str
    run_id: str
    seed: int
    as_of: str
    data_class: str
    disclaimer: str
    units: tuple[UnitAssessment, ...]
    all_observations: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "run_id": self.run_id,
            "seed": self.seed,
            "as_of": self.as_of,
            "data_class": self.data_class,
            "disclaimer": self.disclaimer,
            "hazard_id": "landslide",
            "evidence": {
                "gci": "IMPLEMENTED",
                "landslide_phi": "IMPLEMENTED",
                "exposure": "EXPERIMENTAL (site config when present)",
                "vulnerability": "EXPERIMENTAL (site config when present)",
                "operational_risk": "IMPLEMENTED",
                "alert": "IMPLEMENTED (DRAFT only)",
                "field_validation": "NOT CLAIMED",
                "chi": "NOT_IMPLEMENTED",
                "official_alerting": "NOT_IMPLEMENTED",
            },
            "assessments": [unit.to_dict() for unit in self.units],
        }

    def to_geojson(self) -> dict[str, Any]:
        return {
            "type": "FeatureCollection",
            "data_class": self.data_class,
            "run_id": self.run_id,
            "fixture_id": self.fixture_id,
            "hazard_id": "landslide",
            "disclaimer": self.disclaimer,
            "features": [
                {
                    "type": "Feature",
                    "geometry": unit.observation.geometry,
                    "properties": {
                        "spatial_unit_id": unit.spatial_unit_id,
                        "phi": unit.phi.value,
                        "operational_risk": unit.operational_risk.value,
                        "alert_level": unit.alert.level,
                        "formula_version_phi": unit.phi.formula_version,
                        "disclaimer": DISCLAIMER,
                    },
                }
                for unit in self.units
            ],
        }

    def observations(self) -> list[dict[str, Any]]:
        return list(self.all_observations)


def run_id_for(fixture_id: str, seed: int) -> str:
    return str(uuid5(NAMESPACE_URL, f"polaris:landslide-slice:{fixture_id}:{seed}"))


def _obs_by_unit(observations: tuple[Observation, ...]) -> dict[str, dict[str, Observation]]:
    grouped: dict[str, dict[str, Observation]] = {}
    for obs in observations:
        grouped.setdefault(obs.spatial_unit_id, {})[obs.observed_property] = obs
    return grouped


def assess_landslide_unit(
    *,
    slope_obs: Observation,
    moisture_obs: Observation,
    rain_obs: Observation,
    run_id: str,
    computed_at: str,
) -> UnitAssessment:
    gci = compute_gci(observation=rain_obs, run_id=run_id, computed_at=computed_at)
    accumulation = str(rain_obs.provenance.get("accumulation") or "1h")
    phi = compute_phi(
        slope_deg=slope_obs.value,
        soil_moisture=moisture_obs.value,
        rainfall_mm=rain_obs.value,
        phi_mode=slope_obs.phi_mode,
        spatial_unit_id=slope_obs.spatial_unit_id,
        source_id=slope_obs.source_id,
        observed_at=slope_obs.observed_at,
        computed_at=computed_at,
        quality_flag=slope_obs.quality_flag,
        data_class=slope_obs.data_class,
        run_id=run_id,
        accumulation=accumulation,
    )
    site_id = slope_obs.site_id
    exposure = resolve_exposure(site_id=site_id, spatial_unit_id=slope_obs.spatial_unit_id)
    vulnerability = resolve_vulnerability(
        site_id=site_id, spatial_unit_id=slope_obs.spatial_unit_id
    )
    risk = compute_operational_risk(
        phi=phi,
        exposure=exposure,
        vulnerability=vulnerability,
        computed_at=computed_at,
        ev_config_version=ev_config_version_for_site(site_id),
    )
    alert = build_draft_alert(risk=risk, phi=phi)
    return UnitAssessment(
        spatial_unit_id=slope_obs.spatial_unit_id,
        observation=slope_obs,
        gci=gci,
        phi=phi,
        exposure=exposure,
        vulnerability=vulnerability,
        operational_risk=risk,
        alert=alert,
    )


def run_landslide_slice(fixture: dict[str, Any], *, seed: int = 42) -> LandslideSliceResult:
    fixture_id, as_of, observations = parse_fixture(fixture)
    run_id = run_id_for(fixture_id, seed)
    by_unit = _obs_by_unit(tuple(observations))
    units_list: list[UnitAssessment] = []
    for spatial_unit_id, props in by_unit.items():
        slope = props.get("slope_deg")
        moisture = props.get("soil_moisture")
        rain = props.get("rainfall_mm")
        if slope is None or moisture is None or rain is None:
            raise ValueError(
                f"landslide slice requires slope_deg, soil_moisture, rainfall_mm "
                f"for unit {spatial_unit_id!r}"
            )
        units_list.append(
            assess_landslide_unit(
                slope_obs=slope,
                moisture_obs=moisture,
                rain_obs=rain,
                run_id=run_id,
                computed_at=as_of,
            )
        )
    if not units_list:
        raise ValueError("landslide slice requires at least one spatial unit")
    data_class = observations[0].data_class if observations else fixture.get("data_class")
    return LandslideSliceResult(
        fixture_id=fixture_id,
        run_id=run_id,
        seed=seed,
        as_of=as_of,
        data_class=str(data_class),
        disclaimer=DISCLAIMER,
        units=tuple(units_list),
        all_observations=tuple(obs.to_dict() for obs in observations),
    )
