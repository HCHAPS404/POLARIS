"""Port for hazard `heat`. Evidence: PLACEHOLDER — registry stub only; no PHI in P5."""

from __future__ import annotations

from typing import Protocol

from domains.provenance.index_record import IndexRecord


class HeatModel(Protocol):
    formula_version: str
    model_version: str

    def phi(
        self,
        *,
        temperature_c: float,
        heat_index_c: float | None,
        spatial_unit_id: str,
        source_id: str,
        observed_at: str,
        computed_at: str,
        quality_flag: str,
        data_class: str,
        run_id: str,
    ) -> IndexRecord: ...
