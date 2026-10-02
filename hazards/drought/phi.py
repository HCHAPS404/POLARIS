"""Drought PHI — precipitation deficit + dry soil moisture (screening only).

formula_version: drought.phi.precip-moisture.v0.1.0

  precip_norm  = clamp((P0 − P30) / (P0 − P1), 0, 1)   P0=120 mm P1=20 mm (30d total)
  moisture_norm = clamp((M0 − θ) / (M0 − M1), 0, 1)    M0=0.35 M1=0.12 (volumetric)
  PHI = max(precip_norm, moisture_norm)
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, PHI_MODES
from domains.provenance.index_record import IndexRecord
from hazards.common.clamp import clamp01

FORMULA_VERSION = "drought.phi.precip-moisture.v0.1.0"
MODEL_VERSION = "drought.baseline.v0.1.0"
HAZARD_ID = "drought"
EVIDENCE = EVIDENCE_IMPLEMENTED

P0_MM_30D = 120.0
P1_MM_30D = 20.0
M0 = 0.35
M1 = 0.12

MODE_UNCERTAINTY: dict[str, float] = {
    "DETECTION": 0.20,
    "NOWCAST": 0.35,
    "FORECAST": 0.50,
}


def phi_from_drought(*, precipitation_mm_30d: float, soil_moisture: float) -> float:
    if precipitation_mm_30d < 0:
        raise ValueError("precipitation_mm_30d must be >= 0")
    if not 0 <= soil_moisture <= 1:
        raise ValueError("soil_moisture must be in [0, 1]")
    precip_norm = clamp01(P0_MM_30D - precipitation_mm_30d, P1_MM_30D, P0_MM_30D)
    moisture_norm = clamp01(M0 - soil_moisture, M1, M0)
    return max(precip_norm, moisture_norm)


def compute_phi(
    *,
    precipitation_mm_30d: float,
    soil_moisture: float,
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
    value = phi_from_drought(
        precipitation_mm_30d=precipitation_mm_30d,
        soil_moisture=soil_moisture,
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
            "precipitation_mm_30d": precipitation_mm_30d,
            "soil_moisture": soil_moisture,
            "p0_mm_30d": P0_MM_30D,
            "p1_mm_30d": P1_MM_30D,
            "m0": M0,
            "m1": M1,
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
        notes=(
            "Precipitation deficit + dry-soil screening index. Not SPI/PDSI. "
            "Not calibrated. E/V excluded."
        ),
    )
