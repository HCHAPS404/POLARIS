"""Minimal GCI (evidence confidence) — formula_version gci.v0.1.0.

GCI = clip(qc_score × completeness × data_class_trust, 0, 1)

qc_score:
  qc_pass=1.00, raw=0.70, unknown=0.40, qc_fail=0.05
data_class_trust (V1):
  SIMULATED=0.65
completeness:
  fraction of required inputs present among
  rainfall_mm, observed_at, source_id, data_class

This is a quality score, not a probability of flooding.
"""

from __future__ import annotations

from domains.common import (
    DATA_CLASS_HISTORICAL_REPLAY,
    DATA_CLASS_LIVE_INTEGRATED,
    DATA_CLASS_SIMULATED,
    EVIDENCE_IMPLEMENTED,
)
from domains.observations.models import Observation
from domains.provenance.index_record import IndexRecord

FORMULA_VERSION = "gci.v0.1.0"
MODEL_VERSION = "gci.minimal.v0.1.0"

QC_SCORE: dict[str, float] = {
    "qc_pass": 1.00,
    "raw": 0.70,
    "unknown": 0.40,
    "qc_fail": 0.05,
}

DATA_CLASS_TRUST: dict[str, float] = {
    DATA_CLASS_SIMULATED: 0.65,
    # Reconstructed from public citations or reanalysis — not a live QC'd gauge feed.
    DATA_CLASS_HISTORICAL_REPLAY: 0.70,
    DATA_CLASS_LIVE_INTEGRATED: 0.80,
}

REQUIRED_INPUTS = ("rainfall_mm", "observed_at", "source_id", "data_class")


def completeness(present: tuple[str, ...]) -> float:
    if not REQUIRED_INPUTS:
        return 0.0
    hits = sum(1 for name in REQUIRED_INPUTS if name in present)
    return hits / len(REQUIRED_INPUTS)


def gci_value(*, quality_flag: str, data_class: str, present: tuple[str, ...]) -> float:
    if quality_flag not in QC_SCORE:
        raise ValueError(f"unknown quality_flag {quality_flag!r}")
    if data_class not in DATA_CLASS_TRUST:
        raise ValueError(f"GCI v0.1.0 has no trust weight for data_class={data_class!r}")
    raw = QC_SCORE[quality_flag] * completeness(present) * DATA_CLASS_TRUST[data_class]
    return max(0.0, min(1.0, raw))


def observation_present_fields(observation: Observation) -> tuple[str, ...]:
    present: list[str] = []
    if observation.value is not None:
        present.append("rainfall_mm")
    if observation.observed_at:
        present.append("observed_at")
    if observation.source_id:
        present.append("source_id")
    if observation.data_class:
        present.append("data_class")
    return tuple(present)


def compute_gci(*, observation: Observation, run_id: str, computed_at: str) -> IndexRecord:
    present = observation_present_fields(observation)
    value = gci_value(
        quality_flag=observation.quality_flag,
        data_class=observation.data_class,
        present=present,
    )
    return IndexRecord(
        index_family="GCI",
        hazard_id=None,
        spatial_unit_id=observation.spatial_unit_id,
        value=value,
        unit="dimensionless",
        evidence=EVIDENCE_IMPLEMENTED,
        formula_version=FORMULA_VERSION,
        model_version=MODEL_VERSION,
        inputs={
            "quality_flag": observation.quality_flag,
            "qc_score": QC_SCORE[observation.quality_flag],
            "completeness": completeness(present),
            "data_class_trust": DATA_CLASS_TRUST[observation.data_class],
            "present_fields": list(present),
            "required_fields": list(REQUIRED_INPUTS),
        },
        source_ids=(observation.source_id,),
        observed_at=observation.observed_at,
        computed_at=computed_at,
        quality_flags=(observation.quality_flag,),
        uncertainty=round(1.0 - value, 6),
        data_class=observation.data_class,
        run_id=run_id,
        notes="GCI is evidence confidence, not flood probability.",
    )
