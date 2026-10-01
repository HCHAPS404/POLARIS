"""Flood plugin metadata after V1 baseline."""

from hazards.flood.phi import EVIDENCE, FORMULA_VERSION, HAZARD_ID
from hazards.flood.placeholder import describe


def test_flood_plugin_is_implemented_baseline() -> None:
    meta = describe()
    assert meta["hazard_id"] == HAZARD_ID == "flood"
    assert meta["evidence"] == EVIDENCE == "IMPLEMENTED"
    assert meta["formula_version"] == FORMULA_VERSION
    assert "not-implemented" not in meta["formula_version"]
