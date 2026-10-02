"""Port for hazard `tsunami`. Evidence: IMPLEMENTED event-triggered wave PHI."""

from __future__ import annotations

from typing import Protocol

from domains.provenance.index_record import IndexRecord


class TsunamiModel(Protocol):
    formula_version: str
    model_version: str

    def phi(
        self,
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
    ) -> IndexRecord: ...
