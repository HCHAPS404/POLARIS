"""Flash-flood PHI — intense short-window rainfall burst (not hydrodynamic routing).

formula_version: flash_flood.phi.rain-burst.v0.1.0

  PHI = clamp((R − T0) / (T1 − T0), 0, 1)   T0=25 mm T1=60 mm (declared 1h window)

Steeper thresholds than riverine flood baseline. Exposure/vulnerability excluded.
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, PHI_MODES
from domains.provenance.index_record import IndexRecord
from hazards.common.clamp import clamp01

FORMULA_VERSION = "flash_flood.phi.rain-burst.v0.1.0"
MODEL_VERSION = "flash_flood.baseline.v0.1.0"
HAZARD_ID = "flash_flood"
EVIDENCE = EVIDENCE_IMPLEMENTED

T0_MM = 25.0
T1_MM = 60.0

MODE_UNCERTAINTY: dict[str, float] = {
    "DETECTION": 0.17,
    "NOWCAST": 0.30,
    "FORECAST": 0.44,
}


def phi_from_rainfall_burst(rainfall_mm: float) -> float:
    if rainfall_mm < 0:
        raise ValueError("rainfall_mm must be >= 0")
    return clamp01(rainfall_mm, T0_MM, T1_MM)


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
    value = phi_from_rainfall_burst(rainfall_mm)
    notes = (
        "Rain-burst flash-flood screening index. Not hydrodynamic. Not official warning. "
        "E/V excluded from PHI."
    )
    if accumulation != "1h":
        notes += f" Thresholds are 1h demo values applied to accumulation={accumulation}."
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
