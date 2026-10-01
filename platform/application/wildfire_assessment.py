"""Wildfire slice: observation → GCI → PHI → operational risk → DRAFT alert."""

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
from hazards.wildfire.phi import compute_phi


@dataclass(frozen=True)
class WildfireSliceResult:
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
            "hazard_id": "wildfire",
            "evidence": {
                "gci": "IMPLEMENTED",
                "wildfire_phi": "IMPLEMENTED",
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


def run_id_for(fixture_id: str, seed: int) -> str:
    return str(uuid5(NAMESPACE_URL, f"polaris:wildfire-slice:{fixture_id}:{seed}"))


def _obs_by_unit(observations: tuple[Observation, ...]) -> dict[str, dict[str, Observation]]:
    grouped: dict[str, dict[str, Observation]] = {}
    for obs in observations:
        grouped.setdefault(obs.spatial_unit_id, {})[obs.observed_property] = obs
    return grouped


def assess_wildfire_unit(
    *,
    temp_obs: Observation,
    rh_obs: Observation,
    wind_obs: Observation,
    pm_obs: Observation | None,
    run_id: str,
    computed_at: str,
) -> UnitAssessment:
    gci = compute_gci(observation=temp_obs, run_id=run_id, computed_at=computed_at)
    phi = compute_phi(
        temperature_c=temp_obs.value,
        relative_humidity=rh_obs.value,
        wind_speed_ms=wind_obs.value,
        pm25_ugm3=pm_obs.value if pm_obs else None,
        phi_mode=temp_obs.phi_mode,
        spatial_unit_id=temp_obs.spatial_unit_id,
        source_id=temp_obs.source_id,
        observed_at=temp_obs.observed_at,
        computed_at=computed_at,
        quality_flag=temp_obs.quality_flag,
        data_class=temp_obs.data_class,
        run_id=run_id,
    )
    site_id = temp_obs.site_id
    exposure = resolve_exposure(site_id=site_id, spatial_unit_id=temp_obs.spatial_unit_id)
    vulnerability = resolve_vulnerability(
        site_id=site_id, spatial_unit_id=temp_obs.spatial_unit_id
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
        spatial_unit_id=temp_obs.spatial_unit_id,
        observation=temp_obs,
        gci=gci,
        phi=phi,
        exposure=exposure,
        vulnerability=vulnerability,
        operational_risk=risk,
        alert=alert,
    )


def run_wildfire_slice(fixture: dict[str, Any], *, seed: int = 42) -> WildfireSliceResult:
    fixture_id, as_of, observations = parse_fixture(fixture)
    run_id = run_id_for(fixture_id, seed)
    by_unit = _obs_by_unit(tuple(observations))
    units_list: list[UnitAssessment] = []
    for spatial_unit_id, props in by_unit.items():
        temp = props.get("temperature_c")
        rh = props.get("relative_humidity")
        wind = props.get("wind_speed_ms")
        if temp is None or rh is None or wind is None:
            raise ValueError(
                f"wildfire slice requires temperature_c, relative_humidity, wind_speed_ms "
                f"for unit {spatial_unit_id!r}"
            )
        pm = props.get("pm25_ugm3")
        units_list.append(
            assess_wildfire_unit(
                temp_obs=temp,
                rh_obs=rh,
                wind_obs=wind,
                pm_obs=pm,
                run_id=run_id,
                computed_at=as_of,
            )
        )
    if not units_list:
        raise ValueError("wildfire slice requires at least one spatial unit")
    data_class = observations[0].data_class if observations else fixture.get("data_class")
    return WildfireSliceResult(
        fixture_id=fixture_id,
        run_id=run_id,
        seed=seed,
        as_of=as_of,
        data_class=str(data_class),
        disclaimer=DISCLAIMER,
        units=tuple(units_list),
        all_observations=tuple(obs.to_dict() for obs in observations),
    )
