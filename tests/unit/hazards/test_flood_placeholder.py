"""Placeholder tests for hazard `flood`."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "hazards" / "flood"))

from placeholder import EVIDENCE, HAZARD_ID, describe  # noqa: E402


def test_placeholder_metadata() -> None:
    meta = describe()
    assert meta["hazard_id"] == HAZARD_ID == "flood"
    assert meta["evidence"] == EVIDENCE == "PLACEHOLDER"
    assert meta["formula_version"].endswith("not-implemented")
