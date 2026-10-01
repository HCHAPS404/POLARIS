"""Versioned index envelope shared by GCI, PHI, and operational risk."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domains.common import DISCLAIMER


@dataclass(frozen=True)
class IndexRecord:
    index_family: str
    hazard_id: str | None
    spatial_unit_id: str
    value: float
    unit: str
    evidence: str
    formula_version: str
    model_version: str
    inputs: dict[str, Any]
    source_ids: tuple[str, ...]
    observed_at: str
    computed_at: str
    quality_flags: tuple[str, ...]
    uncertainty: float
    data_class: str
    run_id: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "index_family": self.index_family,
            "hazard_id": self.hazard_id,
            "spatial_unit_id": self.spatial_unit_id,
            "value": self.value,
            "unit": self.unit,
            "evidence": self.evidence,
            "formula_version": self.formula_version,
            "model_version": self.model_version,
            "inputs": dict(self.inputs),
            "source_ids": list(self.source_ids),
            "observed_at": self.observed_at,
            "computed_at": self.computed_at,
            "quality_flags": list(self.quality_flags),
            "uncertainty": self.uncertainty,
            "data_class": self.data_class,
            "disclaimer": DISCLAIMER,
            "notes": self.notes,
            "provenance": {
                "run_id": self.run_id,
                "formula_version": self.formula_version,
                "model_version": self.model_version,
                "inputs": dict(self.inputs),
                "source_ids": list(self.source_ids),
                "observed_at": self.observed_at,
                "computed_at": self.computed_at,
                "quality_flags": list(self.quality_flags),
                "uncertainty": self.uncertainty,
                "data_class": self.data_class,
            },
        }
