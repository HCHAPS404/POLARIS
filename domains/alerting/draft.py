"""DRAFT-only decision-support alerts. Never OFFICIAL. Never auto-sent.

Level bands on operational_risk (dimensionless):
  < 0.10  info
  < 0.30  watch
  < 0.55  warning
  >= 0.55 proposed   (still DRAFT, HITL required)

HCI as a full engine is NOT IMPLEMENTED. This mapper is a transparent
threshold table so operators can see why a DRAFT row appeared.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from domains.common import ALERT_STATUS_DRAFT, DISCLAIMER, EVIDENCE_IMPLEMENTED
from domains.provenance.index_record import IndexRecord

FORMULA_VERSION = "alert.draft.v0.1.0"
MODEL_VERSION = "alert.draft.v0.1.0"

LEVEL_INFO = "info"
LEVEL_WATCH = "watch"
LEVEL_WARNING = "warning"
LEVEL_PROPOSED = "proposed"


def draft_level(operational_risk: float) -> str:
    if operational_risk < 0.10:
        return LEVEL_INFO
    if operational_risk < 0.30:
        return LEVEL_WATCH
    if operational_risk < 0.55:
        return LEVEL_WARNING
    return LEVEL_PROPOSED


@dataclass(frozen=True)
class DraftAlert:
    alert_id: str
    status: str
    level: str
    hazard_id: str | None
    spatial_unit_id: str
    human_in_the_loop: bool
    formula_version: str
    model_version: str
    evidence: str
    disclaimer: str
    provenance: dict[str, Any]
    operational_risk_value: float

    def to_dict(self) -> dict[str, Any]:
        if self.status != ALERT_STATUS_DRAFT:
            raise RuntimeError("refusing to serialise a non-DRAFT alert")
        if not self.human_in_the_loop:
            raise RuntimeError("refusing to serialise an alert without HITL")
        return {
            "alert_id": self.alert_id,
            "status": self.status,
            "level": self.level,
            "hazard_id": self.hazard_id,
            "spatial_unit_id": self.spatial_unit_id,
            "human_in_the_loop": True,
            "formula_version": self.formula_version,
            "model_version": self.model_version,
            "evidence": self.evidence,
            "disclaimer": self.disclaimer,
            "operational_risk_value": self.operational_risk_value,
            "provenance": dict(self.provenance),
            "cap": None,
            "official": False,
        }


def build_draft_alert(*, risk: IndexRecord, phi: IndexRecord) -> DraftAlert:
    if risk.index_family != "operational_risk":
        raise ValueError("draft alert requires an operational_risk record")
    alert_id = str(uuid5(NAMESPACE_URL, f"polaris:alert:{risk.run_id}:{risk.spatial_unit_id}"))
    return DraftAlert(
        alert_id=alert_id,
        status=ALERT_STATUS_DRAFT,
        level=draft_level(risk.value),
        hazard_id=phi.hazard_id,
        spatial_unit_id=risk.spatial_unit_id,
        human_in_the_loop=True,
        formula_version=FORMULA_VERSION,
        model_version=MODEL_VERSION,
        evidence=EVIDENCE_IMPLEMENTED,
        disclaimer=DISCLAIMER,
        operational_risk_value=risk.value,
        provenance={
            "run_id": risk.run_id,
            "formula_version": FORMULA_VERSION,
            "model_version": MODEL_VERSION,
            "inputs": {
                "operational_risk": risk.value,
                "operational_risk_formula_version": risk.formula_version,
                "phi_value": phi.value,
                "phi_formula_version": phi.formula_version,
                "level_table": {
                    "info": "<0.10",
                    "watch": "<0.30",
                    "warning": "<0.55",
                    "proposed": ">=0.55",
                },
            },
            "source_ids": list(risk.source_ids),
            "observed_at": risk.observed_at,
            "computed_at": risk.computed_at,
            "quality_flags": list(risk.quality_flags),
            "uncertainty": risk.uncertainty,
            "data_class": risk.data_class,
        },
    )
