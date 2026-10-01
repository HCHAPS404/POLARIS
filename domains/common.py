"""Shared domain constants. No I/O, no FastAPI."""

from __future__ import annotations

DISCLAIMER = (
    "POLARIS is decision-support research software, not an official warning service. "
    "Outputs must not be treated as evacuation orders or CAP/OFFICIAL alerts. "
    "A human operator must review every DRAFT alert before any operational action."
)

EVIDENCE_IMPLEMENTED = "IMPLEMENTED"
EVIDENCE_DESIGNED = "DESIGNED"
EVIDENCE_PLACEHOLDER = "PLACEHOLDER"
EVIDENCE_NOT_IMPLEMENTED = "NOT_IMPLEMENTED"

DATA_CLASS_SIMULATED = "SIMULATED"
ALLOWED_DATA_CLASSES_V1 = frozenset({DATA_CLASS_SIMULATED})

PHI_MODES = frozenset({"DETECTION", "NOWCAST", "FORECAST"})
QUALITY_FLAGS = frozenset({"unknown", "raw", "qc_pass", "qc_fail"})

HAZARD_FLOOD = "flood"
ALERT_STATUS_DRAFT = "DRAFT"
