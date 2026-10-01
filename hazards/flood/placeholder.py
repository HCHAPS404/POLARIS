"""Placeholder implementation for `flood`."""

from __future__ import annotations

FORMULA_VERSION = "0.0.0-not-implemented"
HAZARD_ID = "flood"
EVIDENCE = "PLACEHOLDER"


def describe() -> dict[str, str]:
    return {
        "hazard_id": HAZARD_ID,
        "formula_version": FORMULA_VERSION,
        "evidence": EVIDENCE,
    }
