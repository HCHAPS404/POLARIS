"""Port for hazard `flood`. Evidence: IMPLEMENTED rainfall-threshold PHI baseline."""

from __future__ import annotations

from typing import Protocol

from domains.provenance.index_record import IndexRecord


class FloodModel(Protocol):
    formula_version: str
    model_version: str

    def phi(
        self,
        rainfall_mm: float,
        *,
        phi_mode: str,
        spatial_unit_id: str,
        source_id: str,
        observed_at: str,
        computed_at: str,
        quality_flag: str,
        data_class: str,
        run_id: str,
    ) -> IndexRecord: ...
