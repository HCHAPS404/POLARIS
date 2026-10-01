"""In-memory observation repository for tests and no-DB dev."""

from __future__ import annotations

from typing import Any


class MemoryObservationRepository:
    def __init__(self) -> None:
        self._observations: dict[str, dict[str, Any]] = {}
        self._by_run: dict[str, list[str]] = {}
        self._assessments: dict[str, dict[str, Any]] = {}

    def is_available(self) -> bool:
        return True

    def clear(self) -> None:
        self._observations.clear()
        self._by_run.clear()
        self._assessments.clear()

    def save_observations(self, *, run_id: str, observations: list[dict[str, Any]]) -> int:
        ids: list[str] = []
        for item in observations:
            oid = str(item["observation_id"])
            self._observations[oid] = dict(item)
            ids.append(oid)
        self._by_run[run_id] = ids
        return len(ids)

    def save_assessment_snapshot(
        self, *, run_id: str, fixture_id: str, snapshot: dict[str, Any]
    ) -> None:
        self._assessments[run_id] = {
            "run_id": run_id,
            "fixture_id": fixture_id,
            "snapshot": snapshot,
        }

    def list_observations(
        self, *, run_id: str | None = None, limit: int = 500
    ) -> list[dict[str, Any]]:
        if run_id is not None:
            ids = self._by_run.get(run_id, [])
            return [self._observations[i] for i in ids[:limit] if i in self._observations]
        items = list(self._observations.values())
        return items[:limit]

    def get_observation(self, observation_id: str) -> dict[str, Any] | None:
        return self._observations.get(observation_id)

    def get_assessment_snapshot(self, run_id: str) -> dict[str, Any] | None:
        row = self._assessments.get(run_id)
        if row is None:
            return None
        return row["snapshot"]
