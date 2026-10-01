"""Load SIMULATED JSON fixtures. Never fabricates LIVE observations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIXTURE = ROOT / "data" / "synthetic" / "flood-bogota-demo.simulated.json"

FIXTURES: dict[str, Path] = {
    "flood-bogota-demo": DEFAULT_FIXTURE,
}


class FixtureNotFoundError(FileNotFoundError):
    """Named SIMULATED fixture is missing."""


def load_simulated_fixture(fixture_id: str | None = None) -> dict[str, Any]:
    path = FIXTURES.get(fixture_id or "flood-bogota-demo", DEFAULT_FIXTURE)
    if not path.is_file():
        raise FixtureNotFoundError(f"SIMULATED fixture not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("data_class") != "SIMULATED":
        raise ValueError(f"refusing to load fixture without data_class=SIMULATED: {path}")
    return payload
