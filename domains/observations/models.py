"""Typed observation. V1 accepts SIMULATED fixtures only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Observation:
    observation_id: str
    observed_at: str
    observed_property: str
    value: float
    unit: str
    quality_flag: str
    source_id: str
    source: str
    data_class: str
    spatial_unit_id: str
    site_id: str
    country_iso: str
    phi_mode: str
    geometry: dict[str, Any]
    provenance: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "observed_at": self.observed_at,
            "observed_property": self.observed_property,
            "value": self.value,
            "unit": self.unit,
            "quality_flag": self.quality_flag,
            "source_id": self.source_id,
            "source": self.source,
            "data_class": self.data_class,
            "spatial_unit_id": self.spatial_unit_id,
            "site_id": self.site_id,
            "country_iso": self.country_iso,
            "phi_mode": self.phi_mode,
            "geometry": self.geometry,
            "provenance": dict(self.provenance),
        }
