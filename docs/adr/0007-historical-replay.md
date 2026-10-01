# ADR-0007 — Historical replay of a documented flood event

**Evidence:** IMPLEMENTED (pipeline + tests). Backtest evidence is **EXPERIMENTAL**, not HISTORICALLY_VALIDATED.

## Status

Accepted — 2026-10-01

## Context

V1 implemented versioned flood PHI, GCI, operational risk, and DRAFT alerts on a
SIMULATED Bogotá fixture. The engineering contract requires a third demonstration:
a documented past rainfall/flood event replayed through the **same** formulas,
with honest hit/miss metrics.

Bogotá April 2011 (río Bogotá / jarillones) is geographically closer to the
INTEGRATION CASE but is a multi-day fluvial overflow; ERA5 1-hour fields over
Bogotá for late April 2011 stay well below the V1 10 mm T0. Mocoa 31 Mar–1 Apr
2017 has public, citable 3-hour and 24-hour station totals plus unambiguous
urban inundation in official Colombian sources, plus a legally fetchable ERA5
hour that **does not** reproduce the burst.

## Decision

1. Add `data_class=HISTORICAL_REPLAY` beside `SIMULATED`. `LIVE` remains refused.
2. `observed_at` **is** `provenance.event_time`. Ingest timestamps must not replace it.
3. Replay **Mocoa 2017** through `flood.phi.rainfall-threshold.v0.1.0`, `gci.v0.1.0`,
   and `risk.operational.phi-ev-stub.v0.1.0`.
4. Score hits when PHI ≥ 0.5 (declared baseline, midpoint of T0/T1).
5. Publish POD only with documented positives; omit FAR when there is no
   documented non-event unit; omit Brier because PHI is not a probability.
6. Label evidence **EXPERIMENTAL**. Do not claim HISTORICALLY_VALIDATED.

## Consequences

Horizon can load `?fixture_id=flood-mocoa-2017-replay`. The Digital Testbed
gains `python -m harness.backtesting.replay --seed 42`. CHI, live adapters,
CAP/OFFICIAL, and additional hazards stay out of scope.

## Validation

Determinism (seed 42), fixture → metrics e2e, LIVE refusal, event_time ≠ ingest.
