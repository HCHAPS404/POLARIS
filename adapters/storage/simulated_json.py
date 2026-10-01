"""Load SIMULATED or HISTORICAL_REPLAY JSON fixtures. Never fabricates LIVE."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from domains.common import ALLOWED_DATA_CLASSES, DATA_CLASS_LIVE, DATA_CLASS_SIMULATED

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIXTURE = ROOT / "data" / "synthetic" / "flood-bogota-demo.simulated.json"

FIXTURES: dict[str, Path] = {
    "flood-bogota-demo": DEFAULT_FIXTURE,
    "flood-mocoa-2017-replay": ROOT / "data" / "historical" / "flood-mocoa-2017.replay.json",
    "landslide-co-slope-demo": ROOT
    / "data"
    / "synthetic"
    / "landslide-co-slope-demo.simulated.json",
    "landslide-co-bogota-demo": ROOT
    / "data"
    / "synthetic"
    / "landslide-co-bogota-demo.simulated.json",
}


class FixtureNotFoundError(FileNotFoundError):
    """Named fixture is missing."""


def load_fixture(fixture_id: str | None = None) -> dict[str, Any]:
    key = fixture_id or "flood-bogota-demo"
    path = FIXTURES.get(key)
    if path is None:
        raise FixtureNotFoundError(f"unknown fixture_id {key!r}")
    if not path.is_file():
        raise FixtureNotFoundError(f"fixture not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    data_class = payload.get("data_class")
    if data_class == DATA_CLASS_LIVE:
        raise ValueError(f"refusing to load LIVE-labelled fixture: {path}")
    if data_class not in ALLOWED_DATA_CLASSES:
        raise ValueError(f"refusing fixture with data_class={data_class!r}: {path}")
    return payload


def load_simulated_fixture(fixture_id: str | None = None) -> dict[str, Any]:
    payload = load_fixture(fixture_id)
    if payload.get("data_class") != DATA_CLASS_SIMULATED:
        raise ValueError(
            f"load_simulated_fixture requires data_class=SIMULATED, got {payload.get('data_class')}"
        )
    return payload
