"""Shared clamp helper for hazard PHI baselines. Evidence: IMPLEMENTED."""

from __future__ import annotations


def clamp01(x: float, lo: float, hi: float) -> float:
    if x <= lo:
        return 0.0
    if x >= hi:
        return 1.0
    return (x - lo) / (hi - lo)
