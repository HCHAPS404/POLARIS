"""Shared slice result shape for baseline hazard assessments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from application.flood_assessment import UnitAssessment
from domains.common import DISCLAIMER


@dataclass(frozen=True)
class BaselineHazardSliceResult:
    hazard_id: str
    fixture_id: str
    run_id: str
    seed: int
    as_of: str
    data_class: str
    disclaimer: str
    units: tuple[UnitAssessment, ...]
    all_observations: tuple[dict[str, Any], ...]
    evidence_block: dict[str, str]
    phi_evidence_key: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "run_id": self.run_id,
            "seed": self.seed,
            "as_of": self.as_of,
            "data_class": self.data_class,
            "disclaimer": self.disclaimer,
            "hazard_id": self.hazard_id,
            "evidence": self.evidence_block,
            "assessments": [unit.to_dict() for unit in self.units],
        }

    def to_geojson(self) -> dict[str, Any]:
        return {
            "type": "FeatureCollection",
            "data_class": self.data_class,
            "run_id": self.run_id,
            "fixture_id": self.fixture_id,
            "hazard_id": self.hazard_id,
            "disclaimer": self.disclaimer,
            "features": [
                {
                    "type": "Feature",
                    "geometry": unit.observation.geometry,
                    "properties": {
                        "spatial_unit_id": unit.spatial_unit_id,
                        "data_class": unit.observation.data_class,
                        "phi_mode": unit.observation.phi_mode,
                        "observed_at": unit.observation.observed_at,
                        "phi": unit.phi.value,
                        "gci": unit.gci.value,
                        "operational_risk": unit.operational_risk.value,
                        "alert_status": unit.alert.status,
                        "alert_level": unit.alert.level,
                        "formula_version_phi": unit.phi.formula_version,
                        "formula_version_gci": unit.gci.formula_version,
                        "formula_version_risk": unit.operational_risk.formula_version,
                        "uncertainty_phi": unit.phi.uncertainty,
                        "quality_flag": unit.observation.quality_flag,
                        "disclaimer": DISCLAIMER,
                    },
                }
                for unit in self.units
            ],
        }

    def observations(self) -> list[dict[str, Any]]:
        return list(self.all_observations)


def baseline_evidence(phi_key: str) -> dict[str, str]:
    return {
        "gci": "IMPLEMENTED",
        phi_key: "IMPLEMENTED",
        "exposure": "EXPERIMENTAL (site config when present)",
        "vulnerability": "EXPERIMENTAL (site config when present)",
        "operational_risk": "IMPLEMENTED",
        "alert": "IMPLEMENTED (DRAFT only)",
        "field_validation": "NOT CLAIMED",
        "chi": "NOT_IMPLEMENTED",
        "official_alerting": "NOT_IMPLEMENTED",
    }
