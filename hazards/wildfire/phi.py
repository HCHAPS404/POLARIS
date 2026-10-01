"""Wildfire PHI baseline — fire-weather susceptibility + optional PM detection.

formula_version: wildfire.phi.fire-weather-pm.v0.1.0

Transparent demo index (NOT field-validated, NOT FWI/NFDRS calibrated):

  temp_norm  = clamp((T − T0) / (T1 − T0), 0, 1)           T0=22°C T1=38°C
  rh_norm    = clamp((RH0 − RH) / (RH0 − RH1), 0, 1)       RH dry-side: RH0=0.55 RH1=0.20 (fraction)
  wind_norm  = clamp((W − W0) / (W1 − W0), 0, 1)           W0=2 m/s W1=14 m/s
  pm_norm    = clamp((PM − PM0) / (PM1 − PM0), 0, 1)       PM0=25 µg/m³ PM1=150 (if PM supplied)

  susceptibility = (temp_norm + rh_norm + wind_norm) / 3
  detection      = pm_norm when pm25_ugm3 is not None, else 0
  PHI            = max(susceptibility, detection)

Low humidity, high temperature, and strong wind raise static susceptibility; elevated PM2.5
supports a detection-oriented signal when air-quality observations exist. Exposure and
vulnerability are excluded from PHI.
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, HAZARD_WILDFIRE, PHI_MODES
from domains.provenance.index_record import IndexRecord

FORMULA_VERSION = "wildfire.phi.fire-weather-pm.v0.1.0"
MODEL_VERSION = "wildfire.baseline.v0.1.0"
HAZARD_ID = HAZARD_WILDFIRE
EVIDENCE = EVIDENCE_IMPLEMENTED

T0_C = 22.0
T1_C = 38.0
RH0 = 0.55
RH1 = 0.20
W0_MS = 2.0
W1_MS = 14.0
PM0_UGM3 = 25.0
PM1_UGM3 = 150.0

MODE_UNCERTAINTY: dict[str, float] = {
    "DETECTION": 0.20,
    "NOWCAST": 0.34,
    "FORECAST": 0.48,
}


def _clamp01(x: float, lo: float, hi: float) -> float:
    if x <= lo:
        return 0.0
    if x >= hi:
        return 1.0
    return (x - lo) / (hi - lo)


def phi_components(
    *,
    temperature_c: float,
    relative_humidity: float,
    wind_speed_ms: float,
    pm25_ugm3: float | None = None,
) -> tuple[float, float, float]:
    if relative_humidity < 0 or relative_humidity > 1:
        raise ValueError("relative_humidity must be in [0, 1]")
    if wind_speed_ms < 0:
        raise ValueError("wind_speed_ms must be >= 0")
    if pm25_ugm3 is not None and pm25_ugm3 < 0:
        raise ValueError("pm25_ugm3 must be >= 0 when provided")
    temp_norm = _clamp01(temperature_c, T0_C, T1_C)
    rh_norm = _clamp01(RH0 - relative_humidity, 0.0, RH0 - RH1)
    wind_norm = _clamp01(wind_speed_ms, W0_MS, W1_MS)
    susceptibility = (temp_norm + rh_norm + wind_norm) / 3.0
    detection = 0.0
    if pm25_ugm3 is not None:
        detection = _clamp01(pm25_ugm3, PM0_UGM3, PM1_UGM3)
    value = max(susceptibility, detection)
    return value, susceptibility, detection


def compute_phi(
    *,
    temperature_c: float,
    relative_humidity: float,
    wind_speed_ms: float,
    pm25_ugm3: float | None,
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
    value, susceptibility, detection = phi_components(
        temperature_c=temperature_c,
        relative_humidity=relative_humidity,
        wind_speed_ms=wind_speed_ms,
        pm25_ugm3=pm25_ugm3,
    )
    notes = (
        "Fire-weather susceptibility with optional PM2.5 detection (max merge). "
        "Not NFDRS/FWI. Not field-validated. E/V excluded from PHI."
    )
    if pm25_ugm3 is None:
        notes += " PM2.5 not supplied; detection term omitted."
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
            "temperature_c": temperature_c,
            "relative_humidity": relative_humidity,
            "wind_speed_ms": wind_speed_ms,
            "pm25_ugm3": pm25_ugm3,
            "temp_norm": _clamp01(temperature_c, T0_C, T1_C),
            "rh_norm": _clamp01(RH0 - relative_humidity, 0.0, RH0 - RH1),
            "wind_norm": _clamp01(wind_speed_ms, W0_MS, W1_MS),
            "susceptibility": susceptibility,
            "detection_pm": detection,
            "merge": "max(susceptibility, detection_pm)",
            "t0_c": T0_C,
            "t1_c": T1_C,
            "rh0": RH0,
            "rh1": RH1,
            "w0_ms": W0_MS,
            "w1_ms": W1_MS,
            "pm0_ugm3": PM0_UGM3,
            "pm1_ugm3": PM1_UGM3,
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
