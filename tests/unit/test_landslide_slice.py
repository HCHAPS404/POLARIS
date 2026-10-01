"""Landslide vertical slice unit tests."""

from __future__ import annotations

from application.landslide_assessment import run_landslide_slice

from adapters.storage.simulated_json import load_fixture


def test_landslide_integration_fixture_pipeline() -> None:
    fixture = load_fixture("landslide-co-slope-demo")
    result = run_landslide_slice(fixture, seed=42)
    assert result.fixture_id == "landslide-co-slope-demo"
    assert len(result.units) == 2
    upper = next(u for u in result.units if u.spatial_unit_id == "co-slope-demo-upper")
    assert upper.phi.formula_version.startswith("landslide.phi.")
    assert upper.exposure.evidence == "EXPERIMENTAL"
    assert upper.alert.status == "DRAFT"
    assert upper.operational_risk.formula_version == "risk.operational.phi-ev-site.v0.1.0"
