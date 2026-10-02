"""Traceable LoRa node energy model (SIMULATED).

States: sleep, sense, tx. Each step records duration and average current for audit.
Evidence: IMPLEMENTED (unit-tested). Not hardware-in-the-loop.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class NodeState(StrEnum):
    SLEEP = "sleep"
    SENSE = "sense"
    TX = "tx"


@dataclass(frozen=True)
class EnergyTraceStep:
    state: NodeState
    duration_ms: float
    current_ma: float

    @property
    def charge_mas(self) -> float:
        return self.current_ma * (self.duration_ms / 1000.0)


@dataclass(frozen=True)
class NodeEnergyProfile:
    sleep_current_ma: float = 0.004
    sense_current_ma: float = 12.0
    tx_current_ma: float = 45.0
    sense_duration_ms: float = 25.0
    tx_duration_ms: float = 80.0
    sleep_between_ms: float = 120.0


@dataclass(frozen=True)
class NodeEnergyReport:
    profile: NodeEnergyProfile
    cycles: int
    trace: tuple[EnergyTraceStep, ...]

    @property
    def total_charge_mas(self) -> float:
        return sum(step.charge_mas for step in self.trace)

    def to_dict(self) -> dict[str, Any]:
        by_state: dict[str, float] = {s.value: 0.0 for s in NodeState}
        for step in self.trace:
            by_state[step.state.value] += step.charge_mas
        return {
            "evidence": "IMPLEMENTED (SIMULATED trace)",
            "cycles": self.cycles,
            "total_charge_mas": round(self.total_charge_mas, 6),
            "charge_mas_by_state": {k: round(v, 6) for k, v in by_state.items()},
            "trace": [
                {
                    "state": step.state.value,
                    "duration_ms": step.duration_ms,
                    "current_ma": step.current_ma,
                    "charge_mas": round(step.charge_mas, 6),
                }
                for step in self.trace
            ],
        }


def simulate_cycles(*, cycles: int, profile: NodeEnergyProfile | None = None) -> NodeEnergyReport:
    if cycles < 1:
        raise ValueError("cycles must be >= 1")
    prof = profile or NodeEnergyProfile()
    steps: list[EnergyTraceStep] = []
    for _ in range(cycles):
        steps.append(
            EnergyTraceStep(NodeState.SLEEP, prof.sleep_between_ms, prof.sleep_current_ma)
        )
        steps.append(
            EnergyTraceStep(NodeState.SENSE, prof.sense_duration_ms, prof.sense_current_ma)
        )
        steps.append(EnergyTraceStep(NodeState.TX, prof.tx_duration_ms, prof.tx_current_ma))
    return NodeEnergyReport(profile=prof, cycles=cycles, trace=tuple(steps))
