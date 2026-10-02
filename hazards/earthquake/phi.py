"""Earthquake PHI — observed shaking only (RAPID_DETECTION / EEW). NO prediction.

formula_version: earthquake.phi.pga-shaking.v0.1.0

Allowed phi_mode: RAPID_DETECTION, EEW only (declared on observation).

  PHI = clamp((PGA − G0) / (G1 − G0), 0, 1)   G0=0.02 g G1=0.30 g

This reflects instrumented or EEW-reported peak ground acceleration, not forecast
magnitude or rupture prediction.
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, PHI_MODES_EARTHQUAKE
from domains.provenance.index_record import IndexRecord
from hazards.common.clamp import clamp01

FORMULA_VERSION = "earthquake.phi.pga-shaking.v0.1.0"
MODEL_VERSION = "earthquake.baseline.v0.1.0"
HAZARD_ID = "earthquake"
EVIDENCE = EVIDENCE_IMPLEMENTED

G0 = 0.02
G1 = 0.30

MODE_UNCERTAINTY: dict[str, float] = {
    "RAPID_DETECTION": 0.25,
    "EEW": 0.35,
}


def phi_from_pga(pga_g: float) -> float:
    if pga_g < 0:
        raise ValueError("pga_g must be >= 0")
    return clamp01(pga_g, G0, G1)


def compute_phi(
    *,
    pga_g: float,
    phi_mode: str,
    spatial_unit_id: str,
    source_id: str,
    observed_at: str,
    computed_at: str,
    quality_flag: str,
    data_class: str,
    run_id: str,
) -> IndexRecord:
    if phi_mode not in PHI_MODES_EARTHQUAKE:
        modes = sorted(PHI_MODES_EARTHQUAKE)
        raise ValueError(
            f"earthquake phi_mode must be declared in {modes}; got {phi_mode!r}. "
            "FORECAST/NOWCAST are refused (no prediction)."
        )
    value = phi_from_pga(pga_g)
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
            "pga_g": pga_g,
            "g0": G0,
            "g1": G1,
            "phi_mode": phi_mode,
            "prediction_used": False,
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
            "Observed PGA shaking index for RAPID_DETECTION/EEW only. "
            "Not earthquake prediction. Not official EEW. E/V excluded."
        ),
    )
