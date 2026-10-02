"""Heat PHI — air temperature + optional heat-index stress (urban screening).

formula_version: heat.phi.heat-stress.v0.1.0

  temp_norm = clamp((T − T0) / (T1 − T0), 0, 1)              T0=30°C T1=40°C
  hi_norm   = clamp((HI − HI0) / (HI1 − HI0), 0, 1)         when heat_index_c supplied
  PHI = max(temp_norm, hi_norm or 0)
"""

from __future__ import annotations

from domains.common import EVIDENCE_IMPLEMENTED, PHI_MODES
from domains.provenance.index_record import IndexRecord
from hazards.common.clamp import clamp01

FORMULA_VERSION = "heat.phi.heat-stress.v0.1.0"
MODEL_VERSION = "heat.baseline.v0.1.0"
HAZARD_ID = "heat"
EVIDENCE = EVIDENCE_IMPLEMENTED

T0_C = 30.0
T1_C = 40.0
HI0_C = 32.0
HI1_C = 41.0

MODE_UNCERTAINTY: dict[str, float] = {
    "DETECTION": 0.16,
    "NOWCAST": 0.29,
    "FORECAST": 0.43,
}


def phi_from_heat(*, temperature_c: float, heat_index_c: float | None) -> float:
    temp_norm = clamp01(temperature_c, T0_C, T1_C)
    hi_norm = 0.0
    if heat_index_c is not None:
        hi_norm = clamp01(heat_index_c, HI0_C, HI1_C)
    return max(temp_norm, hi_norm)


def compute_phi(
    *,
    temperature_c: float,
    heat_index_c: float | None,
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
    value = phi_from_heat(temperature_c=temperature_c, heat_index_c=heat_index_c)
    notes = (
        "Heat-stress screening index (temperature + optional heat index). "
        "Not WBGT occupational standard. E/V excluded."
    )
    if heat_index_c is None:
        notes += " heat_index_c not supplied; heat-index term omitted."
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
            "heat_index_c": heat_index_c,
            "t0_c": T0_C,
            "t1_c": T1_C,
            "hi0_c": HI0_C,
            "hi1_c": HI1_C,
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
