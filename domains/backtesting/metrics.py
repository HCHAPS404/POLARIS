"""Hit/miss scoring against documented binary inundation.

Declared baseline: a unit is a positive prediction when PHI >= threshold
(default 0.5, i.e. rainfall at or above the midpoint of T0=10 mm and T1=80 mm
in the formula's native 1-hour space).

PHI is dimensionless and is NOT a flood probability. Brier score is therefore
not published (it would treat PHI as a probability, which it is not).

POD is reported only when at least one documented positive exists.
FAR is reported only when at least one documented negative exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domains.common import EVIDENCE_EXPERIMENTAL

DEFAULT_PHI_HIT_THRESHOLD = 0.5


@dataclass(frozen=True)
class UnitScore:
    spatial_unit_id: str
    phi: float
    predicted_positive: bool
    ground_truth_flooded: bool
    outcome: str
    accumulation: str
    rainfall_mm: float
    observed_at: str


@dataclass(frozen=True)
class BacktestReport:
    scenario_id: str
    seed: int
    formula_version_phi: str
    phi_hit_threshold: float
    evidence: str
    hits: int
    misses: int
    false_alarms: int
    correct_rejections: int
    pod: float | None
    far: float | None
    brier: None
    units: tuple[UnitScore, ...]
    limitations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "seed": self.seed,
            "formula_version_phi": self.formula_version_phi,
            "phi_hit_threshold": self.phi_hit_threshold,
            "evidence": self.evidence,
            "counts": {
                "hits": self.hits,
                "misses": self.misses,
                "false_alarms": self.false_alarms,
                "correct_rejections": self.correct_rejections,
                "n": len(self.units),
            },
            "pod": self.pod,
            "far": self.far,
            "brier": self.brier,
            "brier_omitted_reason": (
                "PHI is a dimensionless ranking index, not a probability; "
                "Brier is not published."
            ),
            "units": [
                {
                    "spatial_unit_id": unit.spatial_unit_id,
                    "rainfall_mm": unit.rainfall_mm,
                    "accumulation": unit.accumulation,
                    "observed_at": unit.observed_at,
                    "phi": unit.phi,
                    "predicted_positive": unit.predicted_positive,
                    "ground_truth_flooded": unit.ground_truth_flooded,
                    "outcome": unit.outcome,
                }
                for unit in self.units
            ],
            "limitations": list(self.limitations),
        }


def _outcome(*, predicted: bool, truth: bool) -> str:
    if predicted and truth:
        return "hit"
    if (not predicted) and truth:
        return "miss"
    if predicted and (not truth):
        return "false_alarm"
    return "correct_rejection"


def score_units(
    rows: list[dict[str, Any]],
    *,
    scenario_id: str,
    seed: int,
    formula_version_phi: str,
    phi_hit_threshold: float = DEFAULT_PHI_HIT_THRESHOLD,
    limitations: tuple[str, ...],
    historically_validated: bool = False,
) -> BacktestReport:
    if historically_validated:
        raise ValueError(
            "refusing HISTORICALLY_VALIDATED: this scorer does not attest skill; "
            "callers must keep evidence EXPERIMENTAL unless a later review upgrades it"
        )
    units: list[UnitScore] = []
    hits = misses = false_alarms = correct_rejections = 0
    for row in rows:
        phi = float(row["phi"])
        truth = bool(row["ground_truth_flooded"])
        predicted = phi >= phi_hit_threshold
        outcome = _outcome(predicted=predicted, truth=truth)
        if outcome == "hit":
            hits += 1
        elif outcome == "miss":
            misses += 1
        elif outcome == "false_alarm":
            false_alarms += 1
        else:
            correct_rejections += 1
        units.append(
            UnitScore(
                spatial_unit_id=str(row["spatial_unit_id"]),
                phi=phi,
                predicted_positive=predicted,
                ground_truth_flooded=truth,
                outcome=outcome,
                accumulation=str(row.get("accumulation") or "1h"),
                rainfall_mm=float(row["rainfall_mm"]),
                observed_at=str(row["observed_at"]),
            )
        )
    positives = hits + misses
    predicted_positives = hits + false_alarms
    pod = (hits / positives) if positives else None
    far = (false_alarms / predicted_positives) if predicted_positives else None
    if (false_alarms + correct_rejections) == 0:
        far = None
    return BacktestReport(
        scenario_id=scenario_id,
        seed=seed,
        formula_version_phi=formula_version_phi,
        phi_hit_threshold=phi_hit_threshold,
        evidence=EVIDENCE_EXPERIMENTAL,
        hits=hits,
        misses=misses,
        false_alarms=false_alarms,
        correct_rejections=correct_rejections,
        pod=pod,
        far=far,
        brier=None,
        units=tuple(units),
        limitations=limitations,
    )
