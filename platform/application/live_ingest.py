"""LIVE_INTEGRATED ingest orchestration."""

from __future__ import annotations

from typing import Any

from adapters.data.global_feeds.open_meteo_precip import run_live_precip_slice
from application.persistence import persist_flood_slice


def ingest_live_precipitation(*, site_id: str = "co-bogota-demo", seed: int = 42) -> dict[str, Any]:
    result = run_live_precip_slice(site_id=site_id, seed=seed)
    if result.get("status") == "ok" and result.get("flood_slice"):
        storage = persist_flood_slice(
            run_id=result["run_id"],
            fixture_id=result["flood_slice"]["fixture_id"],
            observations=result["observations"],
            snapshot=result["flood_slice"],
        )
        result["storage"] = storage
    return result
