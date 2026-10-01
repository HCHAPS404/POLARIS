"""Landslide PHI baseline — slope + soil moisture + rainfall (susceptibility / nowcast).

formula_version: landslide.phi.slope-moisture-rain.v0.1.0

Transparent demo physics (NOT field-validated):

  slope_norm   = clamp((slope_deg − S0) / (S1 − S0), 0, 1)   S0=12° S1=38°
  moisture_norm = clamp((θ − M0) / (M1 − M0), 0, 1)         M0=0.30 M1=0.75 (volumetric fraction)
  rain_norm    = clamp((R − R0) / (R1 − R0), 0, 1)           R0=15 mm R1=55 mm (1h)

  susceptibility = (slope_norm + moisture_norm) / 2
  trigger        = rain_norm
  PHI            = max(susceptibility, trigger)   # conservative individual-first merge

Rationale: steep, wet slopes raise static susceptibility; intense short rain adds a
dynamic trigger. This is a screening index, not infinite-slope stability or pore-pressure
modeling. Exposure and vulnerability are excluded from PHI.

Limitations: uniform soil strength, no antecedent rain memory, no depth of failure,
not calibrated to Colombian inventory maps, not HISTORICALLY_VALIDATED.
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, HAZARD_LANDSLIDE, PHI_MODES
from domains.provenance.index_record import IndexRecord

FORMULA_VERSION = "landslide.phi.slope-moisture-rain.v0.1.0"
MODEL_VERSION = "landslide.baseline.v0.1.0"
HAZARD_ID = HAZARD_LANDSLIDE
EVIDENCE = EVIDENCE_IMPLEMENTED

S0_DEG = 12.0
S1_DEG = 38.0
M0 = 0.30
M1 = 0.75
R0_MM = 15.0
R1_MM = 55.0

MODE_UNCERTAINTY: dict[str, float] = {
    "DETECTION": 0.18,
    "NOWCAST": 0.32,
    "FORECAST": 0.45,
}


def _clamp01(x: float, lo: float, hi: float) -> float:
    if x <= lo:
        return 0.0
    if x >= hi:
        return 1.0
    return (x - lo) / (hi - lo)


def phi_components(
    *,
    slope_deg: float,
    soil_moisture: float,
    rainfall_mm: float,
) -> tuple[float, float, float, float]:
    if slope_deg < 0:
        raise ValueError("slope_deg must be >= 0")
    if not 0 <= soil_moisture <= 1:
        raise ValueError("soil_moisture must be in [0, 1]")
    if rainfall_mm < 0:
        raise ValueError("rainfall_mm must be >= 0")
    slope_norm = _clamp01(slope_deg, S0_DEG, S1_DEG)
    moisture_norm = _clamp01(soil_moisture, M0, M1)
    rain_norm = _clamp01(rainfall_mm, R0_MM, R1_MM)
    susceptibility = (slope_norm + moisture_norm) / 2.0
    value = max(susceptibility, rain_norm)
    return value, susceptibility, rain_norm, slope_norm


def compute_phi(
    *,
    slope_deg: float,
    soil_moisture: float,
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
    value, susceptibility, rain_norm, slope_norm = phi_components(
        slope_deg=slope_deg,
        soil_moisture=soil_moisture,
        rainfall_mm=rainfall_mm,
    )
    notes = (
        "Slope–moisture susceptibility with rainfall trigger (max merge). "
        "Not infinite-slope mechanics. Not field-validated. E/V excluded from PHI."
    )
    if accumulation != "1h":
        notes += f" Rain thresholds are 1h demo values applied to accumulation={accumulation}."
    moisture_norm = _clamp01(soil_moisture, M0, M1)
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
            "slope_deg": slope_deg,
            "soil_moisture": soil_moisture,
            "rainfall_mm": rainfall_mm,
            "accumulation": accumulation,
            "slope_norm": slope_norm,
            "moisture_norm": moisture_norm,
            "susceptibility": susceptibility,
            "rain_norm": rain_norm,
            "merge": "max(susceptibility, rain_norm)",
            "s0_deg": S0_DEG,
            "s1_deg": S1_DEG,
            "m0": M0,
            "m1": M1,
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
