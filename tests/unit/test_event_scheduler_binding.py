"""Optional pybind11 binding smoke test (runs when module is built)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "build" / "cpp"


@pytest.mark.skipif(
    os.environ.get("POLARIS_EVENT_SCHEDULER_BUILT") != "1",
    reason="Set POLARIS_EVENT_SCHEDULER_BUILT=1 after cmake BUILD_PYBIND11_BINDINGS=ON",
)
def test_pybind_event_scheduler_order() -> None:
    if str(BUILD) not in sys.path:
        sys.path.insert(0, str(BUILD))
    import polaris_event_scheduler as pes  # type: ignore

    sched = pes.EventScheduler()
    sched.schedule(2.0, 1)
    sched.schedule(1.0, 2)
    sched.schedule(1.0, 1)
    first = sched.pop_next()
    assert first.time == 1.0
    assert first.id == 1
    assert sched.size() == 2
