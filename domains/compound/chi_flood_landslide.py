"""Minimal CHI when flood and landslide PHI co-elevate at the same spatial unit.

See docs/adr/0011-compound-chi-flood-landslide.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domains.common import DISCLAIMER, EVIDENCE_IMPLEMENTED
from domains.provenance.index_record import IndexRecord

FORMULA_VERSION = "compound.chi.flood-landslide-rain-coupling.v0.1.0"
MODEL_VERSION = "compound.chi.v0.1.0"
FLOOD_PHI_MIN = 0.25
LANDSLIDE_PHI_MIN = 0.25


def chi_value(phi_flood: float, phi_landslide: float) -> tuple[float, bool]:
    """Return (chi, interaction_active)."""
    if phi_flood < 0 or phi_landslide < 0:
        raise ValueError("PHI inputs must be >= 0")
    active = phi_flood >= FLOOD_PHI_MIN and phi_landslide >= LANDSLIDE_PHI_MIN
    if not active:
        return 0.0, False
    return phi_flood + phi_landslide - (phi_flood * phi_landslide), True


@dataclass(frozen=True)
class CompoundChiInputs:
    phi_flood: float
    phi_landslide: float
    flood_formula_version: str
    landslide_formula_version: str
    flood_phi_min: float = FLOOD_PHI_MIN
    landslide_phi_min: float = LANDSLIDE_PHI_MIN


def build_chi_record(
    *,
    spatial_unit_id: str,
    inputs: CompoundChiInputs,
    source_ids: tuple[str, ...],
    observed_at: str,
    computed_at: str,
    quality_flags: tuple[str, ...],
    data_class: str,
    run_id: str,
) -> IndexRecord:
    value, active = chi_value(inputs.phi_flood, inputs.phi_landslide)
    return IndexRecord(
        index_family="CHI",
        hazard_id="compound/flood-landslide",
        spatial_unit_id=spatial_unit_id,
        value=round(value, 6),
        unit="dimensionless",
        evidence=EVIDENCE_IMPLEMENTED,
        formula_version=FORMULA_VERSION,
        model_version=MODEL_VERSION,
        inputs={
            "phi_flood": inputs.phi_flood,
            "phi_landslide": inputs.phi_landslide,
            "interaction_active": active,
            "flood_phi_min": inputs.flood_phi_min,
            "landslide_phi_min": inputs.landslide_phi_min,
            "flood_formula_version": inputs.flood_formula_version,
            "landslide_formula_version": inputs.landslide_formula_version,
            "disclaimer": DISCLAIMER,
        },
        source_ids=source_ids,
        observed_at=observed_at,
        computed_at=computed_at,
        quality_flags=quality_flags,
        uncertainty=max(
            0.12,
            (inputs.phi_flood + inputs.phi_landslide) * 0.08 if active else 0.12,
        ),
        data_class=data_class,
        run_id=run_id,
        notes=(
            "Rain-coupled screening CHI; not OFFICIAL; not field-validated."
            if active
            else "Gates not met — individual PHIs reported separately."
        ),
    )


def chi_summary(records: tuple[IndexRecord, ...]) -> dict[str, Any]:
    active = [r for r in records if r.inputs.get("interaction_active")]
    return {
        "formula_version": FORMULA_VERSION,
        "model_version": MODEL_VERSION,
        "units_evaluated": len(records),
        "units_active": len(active),
        "max_chi": max((r.value for r in records), default=0.0),
    }
