"""Hazard model registry."""

from __future__ import annotations

from domains.hazards.registry import get_registry_entry, list_registered_hazards


def test_registry_lists_flood_and_landslide() -> None:
    hazards = list_registered_hazards()
    assert "flood" in hazards
    assert "landslide" in hazards
    entry = get_registry_entry("landslide")
    assert entry.evidence == "IMPLEMENTED"
