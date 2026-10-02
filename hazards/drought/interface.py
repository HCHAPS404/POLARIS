"""Port for hazard `drought`. Evidence: IMPLEMENTED precip-moisture PHI baseline."""

from __future__ import annotations

from typing import Protocol

from domains.provenance.index_record import IndexRecord


class DroughtModel(Protocol):
    formula_version: str
    model_version: str

    def phi(
        self,
        *,
        precipitation_mm_30d: float,
        soil_moisture: float,
        phi_mode: str,
        spatial_unit_id: str,
        source_id: str,
        observed_at: str,
        computed_at: str,
        quality_flag: str,
        data_class: str,
        run_id: str,
    ) -> IndexRecord: ...
