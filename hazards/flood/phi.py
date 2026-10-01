"""Flood PHI rainfall-threshold baseline — formula_version flood.phi.rainfall-threshold.v0.1.0.

Individual-first PHI. Exposure and vulnerability are NOT inputs.

  T0 = 10 mm  (1-hour accumulation): PHI = 0 at or below
  T1 = 80 mm  (1-hour accumulation): PHI = 1 at or above
  PHI = (R − T0) / (T1 − T0)  for T0 < R < T1

phi_mode is DECLARED on the observation (DETECTION | NOWCAST | FORECAST).
It is not inferred from timestamps. Mode only selects an uncertainty band:

  DETECTION 0.15 · NOWCAST 0.28 · FORECAST 0.42

These thresholds are a transparent demo baseline, not a calibrated IDF curve
and not a basin-specific warning criterion.
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, HAZARD_FLOOD, PHI_MODES
from domains.provenance.index_record import IndexRecord

FORMULA_VERSION = "flood.phi.rainfall-threshold.v0.1.0"
MODEL_VERSION = "flood.baseline.v0.1.0"
HAZARD_ID = HAZARD_FLOOD
EVIDENCE = EVIDENCE_IMPLEMENTED

T0_MM = 10.0
T1_MM = 80.0

MODE_UNCERTAINTY: dict[str, float] = {
    "DETECTION": 0.15,
    "NOWCAST": 0.28,
    "FORECAST": 0.42,
}


def phi_from_rainfall(rainfall_mm: float) -> float:
    if rainfall_mm < 0:
        raise ValueError("rainfall_mm must be >= 0")
    if rainfall_mm <= T0_MM:
        return 0.0
    if rainfall_mm >= T1_MM:
        return 1.0
    return (rainfall_mm - T0_MM) / (T1_MM - T0_MM)


def compute_phi(
    *,
    rainfall_mm: float,
    phi_mode: str,
    spatial_unit_id: str,
    source_id: str,
    observed_at: str,
    computed_at: str,
    quality_flag: str,
    data_class: str,
    run_id: str,
    accumulation: str = "1h",
) -> IndexRecord:
    if phi_mode not in PHI_MODES:
        raise ValueError(f"phi_mode must be declared in {sorted(PHI_MODES)}; got {phi_mode!r}")
    value = phi_from_rainfall(rainfall_mm)
    notes = (
        "Rainfall-threshold PHI baseline. Not a hydrodynamic model. "
        "Exposure/vulnerability are excluded from PHI."
    )
    if accumulation != "1h":
        notes += (
            f" T0/T1 are 1-hour demo thresholds applied to accumulation={accumulation}; "
            "this is a declared limitation, not a calibrated IDF."
        )
    return IndexRecord(
        index_family="PHI",
        hazard_id=HAZARD_ID,
        spatial_unit_id=spatial_unit_id,
        value=value,
        unit="dimensionless",
        evidence=EVIDENCE,
        formula_version=FORMULA_VERSION,
        model_version=MODEL_VERSION,
        inputs={
            "rainfall_mm": rainfall_mm,
            "accumulation": accumulation,
            "t0_mm": T0_MM,
            "t1_mm": T1_MM,
            "phi_mode": phi_mode,
            "exposure_used": False,
            "vulnerability_used": False,
            "native_threshold_accumulation": "1h",
        },
        source_ids=(source_id,),
        observed_at=observed_at,
        computed_at=computed_at,
        quality_flags=(quality_flag,),
        uncertainty=MODE_UNCERTAINTY[phi_mode],
        data_class=data_class,
        run_id=run_id,
        notes=notes,
    )
