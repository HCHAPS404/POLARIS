"""Flood + landslide CHI — thin wrapper over CHI engine v0.2 (ADR-0011)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domains.compound import chi_engine
from domains.compound.chi_rules import load_rule
from domains.provenance.index_record import IndexRecord

DEFAULT_RULE_ID = "flood-landslide-rain-coupling"
_RULE = load_rule(DEFAULT_RULE_ID)

FORMULA_VERSION = _RULE.formula_version
MODEL_VERSION = _RULE.model_version
FLOOD_PHI_MIN = _RULE.phi_min_for("flood")
LANDSLIDE_PHI_MIN = _RULE.phi_min_for("landslide")


def chi_value(phi_flood: float, phi_landslide: float) -> tuple[float, bool]:
    return chi_engine.evaluate_chi(phi_a=phi_flood, phi_b=phi_landslide, rule=_RULE)


@dataclass(frozen=True)
class CompoundChiInputs:
    phi_flood: float
    phi_landslide: float
    flood_formula_version: str
    landslide_formula_version: str
    flood_phi_min: float = FLOOD_PHI_MIN
    landslide_phi_min: float = LANDSLIDE_PHI_MIN

    def to_engine(self) -> chi_engine.CompoundChiInputs:
        if self.flood_phi_min != FLOOD_PHI_MIN or self.landslide_phi_min != LANDSLIDE_PHI_MIN:
            raise ValueError(
                "custom phi_min gates require chi_engine.build_chi_record with a ChiRule"
            )
        return chi_engine.CompoundChiInputs(
            hazard_ids=("flood", "landslide"),
            phi_values=(self.phi_flood, self.phi_landslide),
            phi_formula_versions=(self.flood_formula_version, self.landslide_formula_version),
            rule_id=DEFAULT_RULE_ID,
        )


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
    return chi_engine.build_chi_record(
        spatial_unit_id=spatial_unit_id,
        inputs=inputs.to_engine(),
        source_ids=source_ids,
        observed_at=observed_at,
        computed_at=computed_at,
        quality_flags=quality_flags,
        data_class=data_class,
        run_id=run_id,
        rule=_RULE,
    )


def chi_summary(records: tuple[IndexRecord, ...]) -> dict[str, Any]:
    return chi_engine.chi_summary(records, rule=_RULE)
