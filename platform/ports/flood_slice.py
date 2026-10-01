"""Interfaces for the flood vertical slice. No FastAPI imports."""

from __future__ import annotations

from typing import Any, Protocol


class SimulatedFixtureSource(Protocol):
    def load(self, fixture_id: str | None = None) -> dict[str, Any]: ...
