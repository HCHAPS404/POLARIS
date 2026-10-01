"""Port for hazard `flood`. Evidence: PLACEHOLDER."""

from __future__ import annotations

from typing import Protocol


class FloodModel(Protocol):
    formula_version: str

    def phi(self, observation: dict) -> None:
        """Intentionally unimplemented in P0."""
        raise NotImplementedError("PHI is not implemented in P0")
