"""CHI engine v0.2 — configurable rules."""

from __future__ import annotations

import pytest
from application.compound_assessment import run_compound_chi

from domains.compound.chi_engine import CompoundChiInputs, build_chi_record, evaluate_chi
from domains.compound.chi_rules import load_rule


def test_union_formula_matches_v01() -> None:
    rule = load_rule("flood-landslide-rain-coupling")
    value, active = evaluate_chi(phi_a=0.5, phi_b=0.6, rule=rule)
    assert active is True
    assert value == pytest.approx(0.5 + 0.6 - 0.5 * 0.6)


def test_build_record_rejects_hazard_mismatch() -> None:
    rule = load_rule("flood-landslide-rain-coupling")
    with pytest.raises(ValueError, match="hazard_ids"):
        build_chi_record(
            spatial_unit_id="u1",
            inputs=CompoundChiInputs(
                hazard_ids=("wildfire", "landslide"),
                phi_values=(0.5, 0.5),
                phi_formula_versions=("a", "b"),
                rule_id=rule.rule_id,
            ),
            source_ids=("s",),
            observed_at="2026-01-01T00:00:00Z",
            computed_at="2026-01-01T00:01:00Z",
            quality_flags=("qc_pass",),
            data_class="SIMULATED",
            run_id="r1",
            rule=rule,
        )


def test_wildfire_landslide_site_runs() -> None:
    result = run_compound_chi(site_id="co-bogota-wildfire-landslide", seed=42)
    assert result.rule.rule_id == "wildfire-landslide-post-fire"
    assert len(result.units) >= 1
    center = next(u for u in result.units if u.spatial_unit_id == "co-bogota-demo-center")
    assert "wildfire" in center.phi_by_hazard
    assert "landslide" in center.phi_by_hazard
