"""Smoke / air-quality PHI — PM2.5 + optional visibility (detection-oriented).

formula_version: smoke.phi.pm-visibility.v0.1.0

  pm_norm  = clamp((PM − PM0) / (PM1 − PM0), 0, 1)     PM0=35 µg/m³ PM1=250
  vis_norm = clamp((V0 − V) / (V0 − V1), 0, 1)         V0=8000 m V1=2000 m (if V supplied)
  PHI = max(pm_norm, vis_norm or 0)
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, PHI_MODES
from domains.provenance.index_record import IndexRecord
from hazards.common.clamp import clamp01

FORMULA_VERSION = "smoke.phi.pm-visibility.v0.1.0"
MODEL_VERSION = "smoke.baseline.v0.1.0"
HAZARD_ID = "smoke"
EVIDENCE = EVIDENCE_IMPLEMENTED

PM0_UGM3 = 35.0
PM1_UGM3 = 250.0
V0_M = 8000.0
V1_M = 2000.0

MODE_UNCERTAINTY: dict[str, float] = {
    "DETECTION": 0.18,
    "NOWCAST": 0.31,
    "FORECAST": 0.46,
}


def phi_from_smoke(*, pm25_ugm3: float, visibility_m: float | None) -> float:
    if pm25_ugm3 < 0:
        raise ValueError("pm25_ugm3 must be >= 0")
    pm_norm = clamp01(pm25_ugm3, PM0_UGM3, PM1_UGM3)
    vis_norm = 0.0
    if visibility_m is not None:
        if visibility_m < 0:
            raise ValueError("visibility_m must be >= 0 when provided")
        vis_norm = clamp01(V0_M - visibility_m, V1_M, V0_M)
    return max(pm_norm, vis_norm)


def compute_phi(
    *,
    pm25_ugm3: float,
    visibility_m: float | None,
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
    value = phi_from_smoke(pm25_ugm3=pm25_ugm3, visibility_m=visibility_m)
    notes = (
        "PM2.5 + optional visibility smoke screening index. "
        "Not dispersion modeling. E/V excluded."
    )
    if visibility_m is None:
        notes += " visibility_m not supplied; visibility term omitted."
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
            "pm25_ugm3": pm25_ugm3,
            "visibility_m": visibility_m,
            "pm0_ugm3": PM0_UGM3,
            "pm1_ugm3": PM1_UGM3,
            "v0_m": V0_M,
            "v1_m": V1_M,
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
