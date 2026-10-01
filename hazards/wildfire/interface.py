"""Port for hazard `wildfire`. Evidence: IMPLEMENTED fire-weather-pm PHI baseline."""

from __future__ import annotations

from typing import Protocol

from domains.provenance.index_record import IndexRecord


class WildfireModel(Protocol):
    formula_version: str
    model_version: str

    def phi(
        self,
        *,
        temperature_c: float,
        relative_humidity: float,
        wind_speed_ms: float,
        pm25_ugm3: float | None,
        phi_mode: str,
        spatial_unit_id: str,
        source_id: str,
        observed_at: str,
        computed_at: str,
        quality_flag: str,
        data_class: str,
        run_id: str,
    ) -> IndexRecord: ...
