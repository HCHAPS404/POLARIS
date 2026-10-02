"""Erosion / subsidence PHI — weak soil + slope + rain (screening).

formula_version: erosion_subsidence.phi.cohesion-slope-rain.v0.1.0

  cohesion_norm = clamp((C0 − c) / (C0 − C1), 0, 1)   c in [0,1] proxy (1=strong)
  slope_norm    = clamp((S − S0) / (S1 − S0), 0, 1)   S0=5° S1=25°
  rain_norm     = clamp((R − R0) / (R1 − R0), 0, 1)   R0=20 mm R1=70 mm (1h)
  susceptibility = (cohesion_norm + slope_norm) / 2
  PHI = max(susceptibility, rain_norm)
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, PHI_MODES
from domains.provenance.index_record import IndexRecord
from hazards.common.clamp import clamp01

FORMULA_VERSION = "erosion_subsidence.phi.cohesion-slope-rain.v0.1.0"
MODEL_VERSION = "erosion_subsidence.baseline.v0.1.0"
HAZARD_ID = "erosion_subsidence"
EVIDENCE = EVIDENCE_IMPLEMENTED

C0 = 0.85
C1 = 0.35
S0_DEG = 5.0
S1_DEG = 25.0
R0_MM = 20.0
R1_MM = 70.0

MODE_UNCERTAINTY: dict[str, float] = {
    "DETECTION": 0.19,
    "NOWCAST": 0.33,
    "FORECAST": 0.47,
}


def phi_from_erosion(
    *,
    soil_cohesion_proxy: float,
    slope_deg: float,
    rainfall_mm: float,
) -> float:
    if not 0 <= soil_cohesion_proxy <= 1:
        raise ValueError("soil_cohesion_proxy must be in [0, 1]")
    if slope_deg < 0:
        raise ValueError("slope_deg must be >= 0")
    if rainfall_mm < 0:
        raise ValueError("rainfall_mm must be >= 0")
    cohesion_norm = clamp01(C0 - soil_cohesion_proxy, C1, C0)
    slope_norm = clamp01(slope_deg, S0_DEG, S1_DEG)
    rain_norm = clamp01(rainfall_mm, R0_MM, R1_MM)
    susceptibility = (cohesion_norm + slope_norm) / 2.0
    return max(susceptibility, rain_norm)


def compute_phi(
    *,
    soil_cohesion_proxy: float,
    slope_deg: float,
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
    value = phi_from_erosion(
        soil_cohesion_proxy=soil_cohesion_proxy,
        slope_deg=slope_deg,
        rainfall_mm=rainfall_mm,
    )
    notes = (
        "Cohesion–slope susceptibility with rainfall trigger (max merge). "
        "Not geotechnical subsidence modeling. E/V excluded."
    )
    if accumulation != "1h":
        notes += f" Rain thresholds are 1h demo values applied to accumulation={accumulation}."
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
            "soil_cohesion_proxy": soil_cohesion_proxy,
            "slope_deg": slope_deg,
            "rainfall_mm": rainfall_mm,
            "accumulation": accumulation,
            "c0": C0,
            "c1": C1,
            "s0_deg": S0_DEG,
            "s1_deg": S1_DEG,
            "r0_mm": R0_MM,
            "r1_mm": R1_MM,
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
