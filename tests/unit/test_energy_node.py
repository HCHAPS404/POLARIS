"""Node energy trace model."""

from __future__ import annotations

import pytest

from simulation.python.energy.node_energy import NodeState, simulate_cycles


def test_three_state_trace_per_cycle() -> None:
    report = simulate_cycles(cycles=2)
    assert report.cycles == 2
    assert len(report.trace) == 6
    assert report.trace[0].state == NodeState.SLEEP
    assert report.trace[1].state == NodeState.SENSE
    assert report.trace[2].state == NodeState.TX
    assert report.total_charge_mas > 0


def test_zero_cycles_rejected() -> None:
    with pytest.raises(ValueError):
        simulate_cycles(cycles=0)
