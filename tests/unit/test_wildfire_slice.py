"""Wildfire vertical slice unit tests."""

from __future__ import annotations

from application.wildfire_assessment import run_wildfire_slice

from adapters.storage.simulated_json import load_fixture


def test_wildfire_integration_fixture_pipeline() -> None:
    fixture = load_fixture("wildfire-co-bogota-demo")
    result = run_wildfire_slice(fixture, seed=42)
    assert result.fixture_id == "wildfire-co-bogota-demo"
    assert len(result.units) == 1
    unit = result.units[0]
    assert unit.phi.formula_version.startswith("wildfire.phi.")
    assert unit.phi.inputs["pm25_ugm3"] == 88.0
    assert unit.alert.status == "DRAFT"
