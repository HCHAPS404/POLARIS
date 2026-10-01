"""Hazard model registry."""

from __future__ import annotations

from domains.hazards.registry import (
    get_registry_entry,
    list_registered_hazards,
    list_registry_hazard_ids,
)


def test_registry_lists_implemented_hazards() -> None:
    hazards = list_registered_hazards()
    assert "flood" in hazards
    assert "landslide" in hazards
    assert "wildfire" in hazards
    entry = get_registry_entry("wildfire")
    assert entry.evidence == "IMPLEMENTED"
    assert entry.formula_version.startswith("wildfire.phi.")
    assert "heat" not in hazards


def test_heat_is_placeholder_in_registry() -> None:
    assert "heat" in list_registry_hazard_ids()
    heat = get_registry_entry("heat")
    assert heat.evidence == "PLACEHOLDER"
