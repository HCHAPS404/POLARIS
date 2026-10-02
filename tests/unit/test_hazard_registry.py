"""Hazard model registry."""

from __future__ import annotations

from domains.hazards.registry import (
    get_registry_entry,
    list_registered_hazards,
    list_registry_hazard_ids,
)


def test_registry_lists_implemented_hazards() -> None:
    hazards = list_registered_hazards()
    for hid in (
        "flood",
        "flash_flood",
        "landslide",
        "wildfire",
        "drought",
        "heat",
        "cyclone",
        "smoke",
        "earthquake",
        "tsunami",
        "volcano",
        "erosion_subsidence",
    ):
        assert hid in hazards
    entry = get_registry_entry("wildfire")
    assert entry.evidence == "IMPLEMENTED"
    assert entry.formula_version.startswith("wildfire.phi.")


def test_heat_is_implemented_in_registry() -> None:
    assert "heat" in list_registry_hazard_ids()
    heat = get_registry_entry("heat")
    assert heat.evidence == "IMPLEMENTED"
    assert heat.formula_version == "heat.phi.heat-stress.v0.1.0"
