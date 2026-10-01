"""PLACEHOLDER exposure stubs. Not calibrated population or asset models.

Values are dimensionless in (0, 1], labelled PLACEHOLDER. They MUST NOT be
folded into PHI.
"""

from __future__ import annotations

from dataclasses import dataclass

from domains.common import EVIDENCE_PLACEHOLDER

FORMULA_VERSION = "exposure.stub.v0.1.0"
MODEL_VERSION = "exposure.stub.v0.1.0"
DEFAULT_EXPOSURE = 0.50

STUB_EXPOSURE: dict[str, float] = {
    "co-bogota-demo-north": 0.40,
    "co-bogota-demo-center": 0.70,
    "co-bogota-demo-south": 0.55,
}


@dataclass(frozen=True)
class ExposureStub:
    spatial_unit_id: str
    value: float
    formula_version: str
    model_version: str
    evidence: str
    notes: str

    def to_dict(self) -> dict[str, str | float]:
        return {
            "spatial_unit_id": self.spatial_unit_id,
            "value": self.value,
            "formula_version": self.formula_version,
            "model_version": self.model_version,
            "evidence": self.evidence,
            "notes": self.notes,
        }


def stub_exposure(spatial_unit_id: str) -> ExposureStub:
    value = STUB_EXPOSURE.get(spatial_unit_id, DEFAULT_EXPOSURE)
    return ExposureStub(
        spatial_unit_id=spatial_unit_id,
        value=value,
        formula_version=FORMULA_VERSION,
        model_version=MODEL_VERSION,
        evidence=EVIDENCE_PLACEHOLDER,
        notes="Uncalibrated stub. Not census, not building stock.",
    )
