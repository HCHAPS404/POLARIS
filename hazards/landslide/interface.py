"""Port for hazard `landslide`. Evidence: IMPLEMENTED slope-moisture-rain PHI baseline."""

from __future__ import annotations

from typing import Protocol

from domains.provenance.index_record import IndexRecord


class LandslideModel(Protocol):
    formula_version: str
    model_version: str

    def phi(
        self,
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
    ) -> IndexRecord: ...
