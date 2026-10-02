"""Volcano PHI — SO2 emission + optional ashfall rate (screening).

formula_version: volcano.phi.so2-ash.v0.1.0

  so2_norm = clamp((SO2 − S0) / (S1 − S0), 0, 1)     S0=500 t/d S1=5000 t/d
  ash_norm = clamp((A − A0) / (A1 − A0), 0, 1)       A0=0.5 mm/h A1=5 mm/h (if supplied)
  PHI = max(so2_norm, ash_norm or 0)
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, PHI_MODES
from domains.provenance.index_record import IndexRecord
from hazards.common.clamp import clamp01

FORMULA_VERSION = "volcano.phi.so2-ash.v0.1.0"
MODEL_VERSION = "volcano.baseline.v0.1.0"
HAZARD_ID = "volcano"
EVIDENCE = EVIDENCE_IMPLEMENTED

S0_TPD = 500.0
S1_TPD = 5000.0
A0_MM_H = 0.5
A1_MM_H = 5.0

MODE_UNCERTAINTY: dict[str, float] = {
    "DETECTION": 0.24,
    "NOWCAST": 0.38,
    "FORECAST": 0.55,
}


def phi_from_volcano(*, so2_ton_per_day: float, ashfall_mm_h: float | None) -> float:
    if so2_ton_per_day < 0:
        raise ValueError("so2_ton_per_day must be >= 0")
    so2_norm = clamp01(so2_ton_per_day, S0_TPD, S1_TPD)
    ash_norm = 0.0
    if ashfall_mm_h is not None:
        if ashfall_mm_h < 0:
            raise ValueError("ashfall_mm_h must be >= 0 when provided")
        ash_norm = clamp01(ashfall_mm_h, A0_MM_H, A1_MM_H)
    return max(so2_norm, ash_norm)


def compute_phi(
    *,
    so2_ton_per_day: float,
    ashfall_mm_h: float | None,
    phi_mode: str,
    spatial_unit_id: str,
    source_id: str,
    observed_at: str,
    computed_at: str,
    quality_flag: str,
    data_class: str,
    run_id: str,
) -> IndexRecord:
    if phi_mode not in PHI_MODES:
        raise ValueError(f"phi_mode must be declared in {sorted(PHI_MODES)}; got {phi_mode!r}")
    value = phi_from_volcano(so2_ton_per_day=so2_ton_per_day, ashfall_mm_h=ashfall_mm_h)
    notes = (
        "SO2 + optional ashfall volcano screening index. "
        "Not plume dispersion or VAAC products. E/V excluded."
    )
    if ashfall_mm_h is None:
        notes += " ashfall_mm_h not supplied; ashfall term omitted."
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
            "so2_ton_per_day": so2_ton_per_day,
            "ashfall_mm_h": ashfall_mm_h,
            "s0_tpd": S0_TPD,
            "s1_tpd": S1_TPD,
            "a0_mm_h": A0_MM_H,
            "a1_mm_h": A1_MM_H,
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
