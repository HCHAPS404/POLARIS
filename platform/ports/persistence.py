"""Persistence ports — observations and assessment snapshots (hexagonal)."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ObservationRepository(Protocol):
    """Store and read observation payloads and assessment JSON snapshots."""

    def is_available(self) -> bool:
        """True when backing storage is configured and reachable."""

    def save_observations(self, *, run_id: str, observations: list[dict[str, Any]]) -> int:
        """Persist observations; returns count written."""

    def save_assessment_snapshot(
        self, *, run_id: str, fixture_id: str, snapshot: dict[str, Any]
    ) -> None:
        """Persist a full flood-slice / assessment payload keyed by run_id."""

    def list_observations(
        self, *, run_id: str | None = None, limit: int = 500
    ) -> list[dict[str, Any]]:
        """List observations, optionally filtered by run_id."""

    def get_observation(self, observation_id: str) -> dict[str, Any] | None:
        """Return one observation dict or None."""

    def get_assessment_snapshot(self, run_id: str) -> dict[str, Any] | None:
        """Return stored assessment snapshot for run_id."""
