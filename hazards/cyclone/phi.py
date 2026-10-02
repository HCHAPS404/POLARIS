"""Cyclone PHI — sustained wind + optional central pressure deficit (screening).

formula_version: cyclone.phi.wind-pressure.v0.1.0

  wind_norm = clamp((W − W0) / (W1 − W0), 0, 1)     W0=17 m/s W1=33 m/s
  pres_norm = clamp((P0 − P) / (P0 − P1), 0, 1)     P0=1013 hPa P1=950 hPa (if P supplied)
  PHI = max(wind_norm, pres_norm or 0)
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, PHI_MODES
from domains.provenance.index_record import IndexRecord
from hazards.common.clamp import clamp01

FORMULA_VERSION = "cyclone.phi.wind-pressure.v0.1.0"
MODEL_VERSION = "cyclone.baseline.v0.1.0"
HAZARD_ID = "cyclone"
EVIDENCE = EVIDENCE_IMPLEMENTED

W0_MS = 17.0
W1_MS = 33.0
P0_HPA = 1013.0
P1_HPA = 950.0

MODE_UNCERTAINTY: dict[str, float] = {
    "DETECTION": 0.22,
    "NOWCAST": 0.36,
    "FORECAST": 0.52,
}


def phi_from_cyclone(*, wind_speed_ms: float, pressure_hpa: float | None) -> float:
    if wind_speed_ms < 0:
        raise ValueError("wind_speed_ms must be >= 0")
    wind_norm = clamp01(wind_speed_ms, W0_MS, W1_MS)
    pres_norm = 0.0
    if pressure_hpa is not None:
        pres_norm = clamp01(P0_HPA - pressure_hpa, P1_HPA, P0_HPA)
    return max(wind_norm, pres_norm)


def compute_phi(
    *,
    wind_speed_ms: float,
    pressure_hpa: float | None,
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
    value = phi_from_cyclone(wind_speed_ms=wind_speed_ms, pressure_hpa=pressure_hpa)
    notes = (
        "Wind + optional pressure-deficit cyclone screening index. "
        "Not a track/intensity forecast model. E/V excluded."
    )
    if pressure_hpa is None:
        notes += " pressure_hpa not supplied; pressure term omitted."
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
            "wind_speed_ms": wind_speed_ms,
            "pressure_hpa": pressure_hpa,
            "w0_ms": W0_MS,
            "w1_ms": W1_MS,
            "p0_hpa": P0_HPA,
            "p1_hpa": P1_HPA,
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
