"""Port for hazard `cyclone`. Evidence: IMPLEMENTED wind-pressure PHI baseline."""

from __future__ import annotations

from typing import Protocol

from domains.provenance.index_record import IndexRecord


class CycloneModel(Protocol):
    formula_version: str
    model_version: str

    def phi(
        self,
        *,
        wind_speed_ms: float,
        pressure_hpa: float | None,
        phi_mode: str,
        spatial_unit_id: str,
        source_id: str,
        observed_at: str,
        computed_at: str,
        quality_flag: str,
        data_class: str,
        run_id: str,
    ) -> IndexRecord: ...
