"""Port for hazard `volcano`. Evidence: IMPLEMENTED SO2-ash PHI baseline."""

from __future__ import annotations

from typing import Protocol

from domains.provenance.index_record import IndexRecord


class VolcanoModel(Protocol):
    formula_version: str
    model_version: str

    def phi(
        self,
        *,
        so2_ton_per_day: float,
        ashfall_mm_h: float | None,
        phi_mode: str,
        spatial_unit_id: str,
        source_id: str,
        observed_at: str,
        computed_at: str,
        quality_flag: str,
        data_class: str,
        run_id: str,
    ) -> IndexRecord: ...
