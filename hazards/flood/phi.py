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
FORMULA_VERSION_RAIN_HYDRO = "flood.phi.rainfall-hydro.v0.2.0"
MODEL_VERSION = "flood.baseline.v0.1.0"
MODEL_VERSION_RAIN_HYDRO = "flood.baseline.v0.2.0"

L0_M = 0.5
L1_M = 3.0
HAZARD_ID = HAZARD_FLOOD
EVIDENCE = EVIDENCE_IMPLEMENTED

T0_MM = 10.0
T1_MM = 80.0

MODE_UNCERTAINTY: dict[str, float] = {
    "DETECTION": 0.15,
    "NOWCAST": 0.28,
    "FORECAST": 0.42,
}


def phi_from_water_level(water_level_m: float) -> float:
    if water_level_m < 0:
        raise ValueError("water_level_m must be >= 0")
    if water_level_m <= L0_M:
        return 0.0
    if water_level_m >= L1_M:
        return 1.0
    return (water_level_m - L0_M) / (L1_M - L0_M)


def combine_rainfall_hydro_phi(phi_rain: float, phi_hydro: float) -> float:
    """Conservative merge: max of individual indices (individual-first, no CHI)."""
    return max(phi_rain, phi_hydro)


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
    return _phi_record(
        value=value,
        formula_version=FORMULA_VERSION,
        model_version=MODEL_VERSION,
        spatial_unit_id=spatial_unit_id,
        phi_mode=phi_mode,
        source_id=source_id,
        observed_at=observed_at,
        computed_at=computed_at,
        quality_flag=quality_flag,
        data_class=data_class,
        run_id=run_id,
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
        notes=notes,
    )


def compute_phi_with_hydro(
    *,
    rainfall_mm: float,
    water_level_m: float | None,
    phi_mode: str,
    spatial_unit_id: str,
    source_id: str,
    observed_at: str,
    computed_at: str,
    quality_flag: str,
    data_class: str,
    run_id: str,
    accumulation: str = "1h",
    hydro_source_id: str | None = None,
) -> IndexRecord:
    if phi_mode not in PHI_MODES:
        raise ValueError(f"phi_mode must be declared in {sorted(PHI_MODES)}; got {phi_mode!r}")
    phi_r = phi_from_rainfall(rainfall_mm)
    if water_level_m is None:
        return compute_phi(
            rainfall_mm=rainfall_mm,
            phi_mode=phi_mode,
            spatial_unit_id=spatial_unit_id,
            source_id=source_id,
            observed_at=observed_at,
            computed_at=computed_at,
            quality_flag=quality_flag,
            data_class=data_class,
            run_id=run_id,
            accumulation=accumulation,
        )
    phi_w = phi_from_water_level(water_level_m)
    value = combine_rainfall_hydro_phi(phi_r, phi_w)
    notes = (
        "Rainfall + water-level threshold PHI baseline (max merge). "
        "Not a hydrodynamic model. Exposure/vulnerability excluded."
    )
    sources = (source_id, hydro_source_id or "hydro/unknown")
    return _phi_record(
        value=value,
        formula_version=FORMULA_VERSION_RAIN_HYDRO,
        model_version=MODEL_VERSION_RAIN_HYDRO,
        spatial_unit_id=spatial_unit_id,
        phi_mode=phi_mode,
        source_id=source_id,
        observed_at=observed_at,
        computed_at=computed_at,
        quality_flag=quality_flag,
        data_class=data_class,
        run_id=run_id,
        source_ids=sources,
        inputs={
            "rainfall_mm": rainfall_mm,
            "water_level_m": water_level_m,
            "phi_rainfall": phi_r,
            "phi_hydro": phi_w,
            "merge": "max",
            "accumulation": accumulation,
            "t0_mm": T0_MM,
            "t1_mm": T1_MM,
            "l0_m": L0_M,
            "l1_m": L1_M,
            "phi_mode": phi_mode,
            "exposure_used": False,
            "vulnerability_used": False,
        },
        notes=notes,
    )


def _phi_record(
    *,
    value: float,
    formula_version: str,
    model_version: str,
    spatial_unit_id: str,
    phi_mode: str,
    source_id: str,
    observed_at: str,
    computed_at: str,
    quality_flag: str,
    data_class: str,
    run_id: str,
    inputs: dict,
    notes: str,
    source_ids: tuple[str, ...] | None = None,
) -> IndexRecord:
    return IndexRecord(
        index_family="PHI",
        hazard_id=HAZARD_ID,
        spatial_unit_id=spatial_unit_id,
        value=value,
        unit="dimensionless",
        evidence=EVIDENCE,
        formula_version=formula_version,
        model_version=model_version,
        inputs=inputs,
        source_ids=source_ids if source_ids is not None else (source_id,),
        observed_at=observed_at,
        computed_at=computed_at,
        quality_flags=(quality_flag,),
        uncertainty=MODE_UNCERTAINTY[phi_mode],
        data_class=data_class,
        run_id=run_id,
        notes=notes,
    )
