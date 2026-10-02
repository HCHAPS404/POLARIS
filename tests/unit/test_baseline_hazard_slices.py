"""Integration: SIMULATED fixtures for new hazard baselines."""

from __future__ import annotations

from adapters.storage.simulated_json import load_fixture
from domains.hazards.registry import run_hazard_slice

NEW_FIXTURES = (
    "flash-flood-co-demo",
    "drought-co-demo",
    "heat-co-demo",
    "cyclone-co-demo",
    "smoke-co-demo",
    "earthquake-co-demo",
    "tsunami-co-demo",
    "volcano-co-demo",
    "erosion-co-demo",
)


def test_all_new_hazard_slices_run() -> None:
    for fixture_id in NEW_FIXTURES:
        fixture = load_fixture(fixture_id)
        result = run_hazard_slice(fixture, seed=42)
        assert result.units
        assert result.units[0].phi.evidence == "IMPLEMENTED"
        geo = result.to_geojson()
        assert geo["type"] == "FeatureCollection"
        assert geo["features"]
