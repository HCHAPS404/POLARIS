"""CHI engine v0.2 — configurable compound rules (ADR-0012)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domains.common import DISCLAIMER, EVIDENCE_IMPLEMENTED
from domains.compound.chi_rules import ChiRule, load_rule
from domains.provenance.index_record import IndexRecord

DEFAULT_RULE_ID = "flood-landslide-rain-coupling"


def _union_value(phi_a: float, phi_b: float) -> float:
    return phi_a + phi_b - (phi_a * phi_b)


def evaluate_chi(
    *,
    phi_a: float,
    phi_b: float,
    rule: ChiRule,
) -> tuple[float, bool]:
    if phi_a < 0 or phi_b < 0:
        raise ValueError("PHI inputs must be >= 0")
    ha, hb = rule.hazard_ids
    active = phi_a >= rule.phi_min_for(ha) and phi_b >= rule.phi_min_for(hb)
    if not active:
        return 0.0, False
    if rule.formula == "union":
        return _union_value(phi_a, phi_b), True
    raise ValueError(f"unsupported formula {rule.formula!r}")


@dataclass(frozen=True)
class CompoundChiInputs:
    hazard_ids: tuple[str, str]
    phi_values: tuple[float, float]
    phi_formula_versions: tuple[str, str]
    rule_id: str = DEFAULT_RULE_ID


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
    rule: ChiRule | None = None,
) -> IndexRecord:
    resolved = rule or load_rule(inputs.rule_id)
    if inputs.hazard_ids != resolved.hazard_ids:
        raise ValueError("hazard_ids must match the loaded rule")
    phi_a, phi_b = inputs.phi_values
    value, active = evaluate_chi(phi_a=phi_a, phi_b=phi_b, rule=resolved)
    ha, hb = resolved.hazard_ids
    return IndexRecord(
        index_family="CHI",
        hazard_id=resolved.compound_hazard_id,
        spatial_unit_id=spatial_unit_id,
        value=round(value, 6),
        unit="dimensionless",
        evidence=EVIDENCE_IMPLEMENTED,
        formula_version=resolved.formula_version,
        model_version=resolved.model_version,
        inputs={
            f"phi_{ha}": phi_a,
            f"phi_{hb}": phi_b,
            "interaction_active": active,
            "rule_id": resolved.rule_id,
            f"phi_min_{ha}": resolved.phi_min_for(ha),
            f"phi_min_{hb}": resolved.phi_min_for(hb),
            f"{ha}_formula_version": inputs.phi_formula_versions[0],
            f"{hb}_formula_version": inputs.phi_formula_versions[1],
            "disclaimer": DISCLAIMER,
        },
        source_ids=source_ids,
        observed_at=observed_at,
        computed_at=computed_at,
        quality_flags=quality_flags,
        uncertainty=max(0.12, (phi_a + phi_b) * 0.08 if active else 0.12),
        data_class=data_class,
        run_id=run_id,
        notes=(
            f"Rule {resolved.rule_id}; screening CHI; not OFFICIAL; not field-validated."
            if active
            else "Gates not met — individual PHIs reported separately."
        ),
    )


def chi_summary(records: tuple[IndexRecord, ...], *, rule: ChiRule) -> dict[str, Any]:
    active = [r for r in records if r.inputs.get("interaction_active")]
    return {
        "rule_id": rule.rule_id,
        "formula_version": rule.formula_version,
        "model_version": rule.model_version,
        "units_evaluated": len(records),
        "units_active": len(active),
        "max_chi": max((r.value for r in records), default=0.0),
    }
