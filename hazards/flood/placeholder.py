"""Flood plugin metadata. PHI baseline lives in phi.py."""

from __future__ import annotations

from .phi import EVIDENCE, FORMULA_VERSION, HAZARD_ID, MODEL_VERSION


def describe() -> dict[str, str]:
    return {
        "hazard_id": HAZARD_ID,
        "formula_version": FORMULA_VERSION,
        "model_version": MODEL_VERSION,
        "evidence": EVIDENCE,
    }
