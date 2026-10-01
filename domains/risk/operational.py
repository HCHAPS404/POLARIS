"""Operational risk = PHI × exposure_stub × vulnerability_stub.

formula_version: risk.operational.phi-ev-stub.v0.1.0

This is a dimensionless ranking index in [0, 1]. It is NOT a probability
('risk = 83%') and NOT a calibrated loss estimate.
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED
from domains.exposure.stub import ExposureStub
from domains.provenance.index_record import IndexRecord
from domains.vulnerability.stub import VulnerabilityStub

FORMULA_VERSION_STUB = "risk.operational.phi-ev-stub.v0.1.0"
FORMULA_VERSION_SITE = "risk.operational.phi-ev-site.v0.1.0"
FORMULA_VERSION = FORMULA_VERSION_STUB
MODEL_VERSION = "risk.operational.v0.1.0"


def operational_risk_value(phi_value: float, exposure: float, vulnerability: float) -> float:
    if min(phi_value, exposure, vulnerability) < 0:
        raise ValueError("PHI, exposure, and vulnerability must be >= 0")
    return phi_value * exposure * vulnerability


def _risk_formula_version(exposure: ExposureStub, vulnerability: VulnerabilityStub) -> str:
    if exposure.formula_version.startswith("exposure.site-config") and (
        vulnerability.formula_version.startswith("vulnerability.site-config")
    ):
        return FORMULA_VERSION_SITE
    return FORMULA_VERSION_STUB


def compute_operational_risk(
    *,
    phi: IndexRecord,
    exposure: ExposureStub,
    vulnerability: VulnerabilityStub,
    computed_at: str,
    ev_config_version: str | None = None,
) -> IndexRecord:
    if phi.index_family != "PHI":
        raise ValueError("operational risk requires a PHI index record")
    if "exposure_used" in phi.inputs and phi.inputs["exposure_used"]:
        raise ValueError("PHI inputs must not already mix exposure")
    value = operational_risk_value(phi.value, exposure.value, vulnerability.value)
    formula_version = _risk_formula_version(exposure, vulnerability)
    ev_note = (
        "Exposure/vulnerability from site YAML (EXPERIMENTAL)."
        if formula_version == FORMULA_VERSION_SITE
        else "Exposure and vulnerability factors are PLACEHOLDER stubs."
    )
    return IndexRecord(
        index_family="operational_risk",
        hazard_id=phi.hazard_id,
        spatial_unit_id=phi.spatial_unit_id,
        value=value,
        unit="dimensionless",
        evidence=EVIDENCE_IMPLEMENTED,
        formula_version=formula_version,
        model_version=MODEL_VERSION,
        inputs={
            "phi_value": phi.value,
            "phi_formula_version": phi.formula_version,
            "exposure_value": exposure.value,
            "exposure_formula_version": exposure.formula_version,
            "exposure_evidence": exposure.evidence,
            "vulnerability_value": vulnerability.value,
            "vulnerability_formula_version": vulnerability.formula_version,
            "vulnerability_evidence": vulnerability.evidence,
            "ev_config_version": ev_config_version,
            "identity": "phi * exposure * vulnerability",
        },
        source_ids=phi.source_ids,
        observed_at=phi.observed_at,
        computed_at=computed_at,
        quality_flags=phi.quality_flags,
        uncertainty=phi.uncertainty,
        data_class=phi.data_class,
        run_id=phi.run_id,
        notes=(
            "Dimensionless operational ranking. Not a probability of impact. " + ev_note
        ),
    )
