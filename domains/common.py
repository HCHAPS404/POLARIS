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
DATA_CLASS_HISTORICAL_REPLAY = "HISTORICAL_REPLAY"
DATA_CLASS_LIVE = "LIVE"
ALLOWED_DATA_CLASSES = frozenset({DATA_CLASS_SIMULATED, DATA_CLASS_HISTORICAL_REPLAY})
ALLOWED_DATA_CLASSES_V1 = ALLOWED_DATA_CLASSES

EVIDENCE_EXPERIMENTAL = "EXPERIMENTAL"
EVIDENCE_HISTORICALLY_VALIDATED = "HISTORICALLY_VALIDATED"

PHI_MODES = frozenset({"DETECTION", "NOWCAST", "FORECAST"})
QUALITY_FLAGS = frozenset({"unknown", "raw", "qc_pass", "qc_fail"})

HAZARD_FLOOD = "flood"
ALERT_STATUS_DRAFT = "DRAFT"
