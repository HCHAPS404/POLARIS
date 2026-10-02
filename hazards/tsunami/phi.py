"""Tsunami PHI — event-triggered coastal wave/run-up screening only.

formula_version: tsunami.phi.event-wave.v0.1.0

Allowed phi_mode: EVENT_TRIGGERED (declared). Requires trigger_event_id on observation provenance
or explicit trigger flag in inputs.

When triggered:
  wave_norm = clamp((H − H0) / (H1 − H0), 0, 1)   H0=0.3 m H1=3.0 m (wave_height_m)
  dist_norm = clamp((D0 − D) / (D0 − D1), 0, 1)   optional distance_km from source
  PHI = max(wave_norm, dist_norm contribution capped at 0.5 when only distance supplied)

When not triggered: PHI = 0 with explicit notes (no standalone forecast).
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, PHI_MODES_TSUNAMI
from domains.provenance.index_record import IndexRecord
from hazards.common.clamp import clamp01

FORMULA_VERSION = "tsunami.phi.event-wave.v0.1.0"
MODEL_VERSION = "tsunami.baseline.v0.1.0"
HAZARD_ID = "tsunami"
EVIDENCE = EVIDENCE_IMPLEMENTED

H0_M = 0.3
H1_M = 3.0
D0_KM = 500.0
D1_KM = 50.0

MODE_UNCERTAINTY: dict[str, float] = {
    "EVENT_TRIGGERED": 0.40,
}


def phi_from_tsunami(
    *,
    event_triggered: bool,
    wave_height_m: float | None,
    distance_km: float | None,
) -> tuple[float, str]:
    if not event_triggered:
        return 0.0, "No trigger declared; tsunami PHI held at 0 (event-triggered mode only)."
    wave_norm = 0.0
    if wave_height_m is not None:
        if wave_height_m < 0:
            raise ValueError("wave_height_m must be >= 0 when provided")
        wave_norm = clamp01(wave_height_m, H0_M, H1_M)
    dist_norm = 0.0
    if distance_km is not None:
        if distance_km < 0:
            raise ValueError("distance_km must be >= 0 when provided")
        dist_norm = clamp01(D0_KM - distance_km, D1_KM, D0_KM) * 0.5
    if wave_height_m is None and distance_km is None:
        return 0.0, "Trigger set but no wave_height_m or distance_km; PHI=0."
    value = max(wave_norm, dist_norm)
    return value, "Event-triggered tsunami screening index. Not inundation modeling."


def compute_phi(
    *,
    event_triggered: bool,
    wave_height_m: float | None,
    distance_km: float | None,
    trigger_event_id: str | None,
    phi_mode: str,
    spatial_unit_id: str,
    source_id: str,
    observed_at: str,
    computed_at: str,
    quality_flag: str,
    data_class: str,
    run_id: str,
) -> IndexRecord:
    if phi_mode not in PHI_MODES_TSUNAMI:
        raise ValueError(
            f"tsunami phi_mode must be {sorted(PHI_MODES_TSUNAMI)}; got {phi_mode!r}"
        )
    value, detail = phi_from_tsunami(
        event_triggered=event_triggered,
        wave_height_m=wave_height_m,
        distance_km=distance_km,
    )
    notes = (
        f"{detail} Not official tsunami warning. No standalone forecast. E/V excluded."
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
            "event_triggered": event_triggered,
            "trigger_event_id": trigger_event_id,
            "wave_height_m": wave_height_m,
            "distance_km": distance_km,
            "h0_m": H0_M,
            "h1_m": H1_M,
            "d0_km": D0_KM,
            "d1_km": D1_KM,
            "phi_mode": phi_mode,
            "forecast_used": False,
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
