"""Flood vertical slice: observation → GCI → PHI → operational risk → DRAFT alert."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from domains.alerting.draft import DraftAlert, build_draft_alert
from domains.common import DISCLAIMER
from domains.exposure.stub import ExposureStub, stub_exposure
from domains.observations.models import Observation
from domains.observations.parse import parse_fixture
from domains.provenance.index_record import IndexRecord
from domains.quality.gci import compute_gci
from domains.risk.operational import compute_operational_risk
from domains.vulnerability.stub import VulnerabilityStub, stub_vulnerability
from hazards.flood.phi import compute_phi


@dataclass(frozen=True)
class UnitAssessment:
    spatial_unit_id: str
    observation: Observation
    gci: IndexRecord
    phi: IndexRecord
    exposure: ExposureStub
    vulnerability: VulnerabilityStub
    operational_risk: IndexRecord
    alert: DraftAlert

    def to_dict(self) -> dict[str, Any]:
        return {
            "spatial_unit_id": self.spatial_unit_id,
            "data_class": self.observation.data_class,
            "disclaimer": DISCLAIMER,
            "observation": self.observation.to_dict(),
            "gci": self.gci.to_dict(),
            "phi": self.phi.to_dict(),
            "exposure": self.exposure.to_dict(),
            "vulnerability": self.vulnerability.to_dict(),
            "operational_risk": self.operational_risk.to_dict(),
            "alert": self.alert.to_dict(),
        }

    def to_geojson_feature(self) -> dict[str, Any]:
        return {
            "type": "Feature",
            "geometry": self.observation.geometry,
            "properties": {
                "spatial_unit_id": self.spatial_unit_id,
                "data_class": self.observation.data_class,
                "phi_mode": self.observation.phi_mode,
                "rainfall_mm": self.observation.value,
                "accumulation": self.observation.provenance.get("accumulation", "1h"),
                "observed_at": self.observation.observed_at,
                "phi": self.phi.value,
                "gci": self.gci.value,
                "operational_risk": self.operational_risk.value,
                "alert_status": self.alert.status,
                "alert_level": self.alert.level,
                "formula_version_phi": self.phi.formula_version,
                "formula_version_gci": self.gci.formula_version,
                "formula_version_risk": self.operational_risk.formula_version,
                "uncertainty_phi": self.phi.uncertainty,
                "quality_flag": self.observation.quality_flag,
                "disclaimer": DISCLAIMER,
            },
        }


@dataclass(frozen=True)
class FloodSliceResult:
    fixture_id: str
    run_id: str
    seed: int
    as_of: str
    data_class: str
    disclaimer: str
    units: tuple[UnitAssessment, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "run_id": self.run_id,
            "seed": self.seed,
            "as_of": self.as_of,
            "data_class": self.data_class,
            "disclaimer": self.disclaimer,
            "evidence": {
                "gci": "IMPLEMENTED",
                "flood_phi": "IMPLEMENTED",
                "exposure": "PLACEHOLDER",
                "vulnerability": "PLACEHOLDER",
                "operational_risk": "IMPLEMENTED",
                "alert": "IMPLEMENTED (DRAFT only)",
                "chi": "NOT_IMPLEMENTED",
                "hci_engine": "NOT_IMPLEMENTED",
                "official_alerting": "NOT_IMPLEMENTED",
                "historical_replay": "IMPLEMENTED (EXPERIMENTAL evidence)",
            },
            "assessments": [unit.to_dict() for unit in self.units],
        }

    def to_geojson(self) -> dict[str, Any]:
        return {
            "type": "FeatureCollection",
            "data_class": self.data_class,
            "run_id": self.run_id,
            "fixture_id": self.fixture_id,
            "disclaimer": self.disclaimer,
            "features": [unit.to_geojson_feature() for unit in self.units],
        }

    def observations(self) -> list[dict[str, Any]]:
        return [unit.observation.to_dict() for unit in self.units]


def run_id_for(fixture_id: str, seed: int) -> str:
    return str(uuid5(NAMESPACE_URL, f"polaris:flood-slice:{fixture_id}:{seed}"))


def assess_observation(
    *, observation: Observation, run_id: str, computed_at: str
) -> UnitAssessment:
    gci = compute_gci(observation=observation, run_id=run_id, computed_at=computed_at)
    accumulation = str(observation.provenance.get("accumulation") or "1h")
    phi = compute_phi(
        rainfall_mm=observation.value,
        phi_mode=observation.phi_mode,
        spatial_unit_id=observation.spatial_unit_id,
        source_id=observation.source_id,
        observed_at=observation.observed_at,
        computed_at=computed_at,
        quality_flag=observation.quality_flag,
        data_class=observation.data_class,
        run_id=run_id,
        accumulation=accumulation,
    )
    exposure = stub_exposure(observation.spatial_unit_id)
    vulnerability = stub_vulnerability(observation.spatial_unit_id)
    risk = compute_operational_risk(
        phi=phi,
        exposure=exposure,
        vulnerability=vulnerability,
        computed_at=computed_at,
    )
    alert = build_draft_alert(risk=risk, phi=phi)
    return UnitAssessment(
        spatial_unit_id=observation.spatial_unit_id,
        observation=observation,
        gci=gci,
        phi=phi,
        exposure=exposure,
        vulnerability=vulnerability,
        operational_risk=risk,
        alert=alert,
    )


def run_flood_slice(fixture: dict[str, Any], *, seed: int = 42) -> FloodSliceResult:
    fixture_id, as_of, observations = parse_fixture(fixture)
    run_id = run_id_for(fixture_id, seed)
    rainfall_obs = [obs for obs in observations if obs.observed_property == "rainfall_mm"]
    if not rainfall_obs:
        raise ValueError("flood slice requires at least one rainfall_mm observation")
    units = tuple(
        assess_observation(observation=obs, run_id=run_id, computed_at=as_of)
        for obs in rainfall_obs
    )
    data_class = observations[0].data_class if observations else fixture.get("data_class")
    return FloodSliceResult(
        fixture_id=fixture_id,
        run_id=run_id,
        seed=seed,
        as_of=as_of,
        data_class=str(data_class),
        disclaimer=DISCLAIMER,
        units=units,
    )
