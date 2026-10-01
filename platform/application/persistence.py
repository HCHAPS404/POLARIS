"""Persist ingest / slice outputs through the storage port."""

from __future__ import annotations

from typing import Any

from adapters.storage.repository_factory import get_observation_repository


def persist_flood_slice(
    *,
    run_id: str,
    fixture_id: str,
    observations: list[dict[str, Any]],
    snapshot: dict[str, Any],
) -> dict[str, str]:
    from adapters.storage.postgis_repository import PostgisObservationRepository

    repo = get_observation_repository()
    written = repo.save_observations(run_id=run_id, observations=observations)
    repo.save_assessment_snapshot(run_id=run_id, fixture_id=fixture_id, snapshot=snapshot)
    backend = "postgis" if isinstance(repo, PostgisObservationRepository) else "memory"
    return {"storage_backend": backend, "observations_persisted": str(written)}
