"""Unit tests for minimal flood–landslide CHI."""

from __future__ import annotations

import pytest
from application.compound_assessment import run_compound_chi

from domains.compound.chi_flood_landslide import (
    FLOOD_PHI_MIN,
    LANDSLIDE_PHI_MIN,
    CompoundChiInputs,
    build_chi_record,
    chi_value,
)


def test_chi_gates_inactive() -> None:
    value, active = chi_value(0.24, 0.9)
    assert active is False
    assert value == 0.0


def test_chi_coupled_formula() -> None:
    pf, pl = 0.5, 0.6
    value, active = chi_value(pf, pl)
    assert active is True
    assert value == pytest.approx(pf + pl - pf * pl)


def test_build_chi_record_provenance() -> None:
    rec = build_chi_record(
        spatial_unit_id="u1",
        inputs=CompoundChiInputs(
            phi_flood=0.4,
            phi_landslide=0.35,
            flood_formula_version="flood.phi.rainfall-threshold.v0.1.0",
            landslide_formula_version="landslide.phi.slope-moisture-rain.v0.1.0",
        ),
        source_ids=("a", "b"),
        observed_at="2026-10-01T12:00:00Z",
        computed_at="2026-10-01T12:01:00Z",
        quality_flags=("qc_pass",),
        data_class="SIMULATED",
        run_id="run-test",
    )
    assert rec.index_family == "CHI"
    assert rec.inputs["interaction_active"] is True
    assert rec.formula_version.startswith("compound.chi.")


def test_compound_site_north_active_south_inactive() -> None:
    result = run_compound_chi(site_id="co-bogota-demo", seed=42)
    by_unit = {u.spatial_unit_id: u for u in result.units}
    north = by_unit["co-bogota-demo-north"]
    south = by_unit["co-bogota-demo-south"]
    assert north.phi_flood >= FLOOD_PHI_MIN
    assert north.phi_landslide >= LANDSLIDE_PHI_MIN
    assert north.chi.inputs["interaction_active"] is True
    assert north.chi.value > 0.5
    assert south.chi.inputs["interaction_active"] is False
    assert south.chi.value == 0.0
