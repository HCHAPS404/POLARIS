"""Generic unit assembly for baseline hazard slices."""

from __future__ import annotations

from application.flood_assessment import UnitAssessment
from domains.alerting.draft import build_draft_alert
from domains.observations.models import Observation
from domains.provenance.index_record import IndexRecord
from domains.quality.gci import compute_gci
from domains.risk.operational import compute_operational_risk
from domains.sites.ev_config import (
    ev_config_version_for_site,
    resolve_exposure,
    resolve_vulnerability,
)


def assess_with_phi(
    *,
    primary_obs: Observation,
    phi: IndexRecord,
    run_id: str,
    computed_at: str,
    gci_obs: Observation | None = None,
) -> UnitAssessment:
    gci_source = gci_obs or primary_obs
    gci = compute_gci(observation=gci_source, run_id=run_id, computed_at=computed_at)
    site_id = primary_obs.site_id
    exposure = resolve_exposure(site_id=site_id, spatial_unit_id=primary_obs.spatial_unit_id)
    vulnerability = resolve_vulnerability(
        site_id=site_id, spatial_unit_id=primary_obs.spatial_unit_id
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
        spatial_unit_id=primary_obs.spatial_unit_id,
        observation=primary_obs,
        gci=gci,
        phi=phi,
        exposure=exposure,
        vulnerability=vulnerability,
        operational_risk=risk,
        alert=alert,
    )


def obs_by_unit(observations: tuple[Observation, ...]) -> dict[str, dict[str, Observation]]:
    grouped: dict[str, dict[str, Observation]] = {}
    for obs in observations:
        grouped.setdefault(obs.spatial_unit_id, {})[obs.observed_property] = obs
    return grouped
