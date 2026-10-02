"""Port for hazard `erosion_subsidence`. Evidence: IMPLEMENTED cohesion-slope-rain PHI."""

from __future__ import annotations

from typing import Protocol

from domains.provenance.index_record import IndexRecord


class ErosionSubsidenceModel(Protocol):
    formula_version: str
    model_version: str

    def phi(
        self,
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
    ) -> IndexRecord: ...
