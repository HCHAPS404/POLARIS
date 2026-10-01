"""Deterministic sim runner: same seed → same PHI/GCI."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "platform"))

from simulation.python.run import run  # noqa: E402


def test_seed_42_is_deterministic() -> None:
    scenario = ROOT / "simulation" / "scenarios" / "flood-bogota-demo.yaml"
    a = run(scenario, 42)
    b = run(scenario, 42)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    north = next(u for u in a["assessments"] if u["spatial_unit_id"] == "co-bogota-demo-north")
    assert north["phi"]["value"] == 62 / 70
    assert north["gci"]["value"] == 0.65
    assert north["alert"]["level"] == "watch"
