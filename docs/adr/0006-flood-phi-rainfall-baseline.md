# ADR-0006 — Flood PHI rainfall-threshold baseline for the V1 vertical slice

**Evidence:** IMPLEMENTED (formula + tests). Exposure/vulnerability remain PLACEHOLDER stubs.

## Status

Accepted — 2026-10-01

## Context

P0 left every hazard plugin as PLACEHOLDER. The first executable slice needs one
transparent flood index, a quality score, an operational ranking, and DRAFT
alerts — without pretending to be a hydrodynamic model, a live gauge network,
or an official warning service.

A previous gap note suggested `packages/indices` + `sim/`. The canonical tree
is `domains/`, `hazards/flood`, and `simulation/`.

## Decision

1. **PHI (flood)** uses a 1-hour rainfall-threshold baseline:
   `PHI = 0` for `R ≤ 10 mm`, `PHI = 1` for `R ≥ 80 mm`, linear in between.
   Formula version: `flood.phi.rainfall-threshold.v0.1.0`.
2. **`phi_mode` is declared** on the observation as `DETECTION` | `NOWCAST` |
   `FORECAST`. Mode selects an uncertainty band only; it is not inferred.
3. **PHI excludes exposure and vulnerability.** Operational risk is
   `PHI × E_stub × V_stub` (`risk.operational.phi-ev-stub.v0.1.0`).
4. **GCI** is `qc_score × completeness × data_class_trust` (`gci.v0.1.0`).
   V1 trust for `SIMULATED` is 0.65. LIVE is refused, not faked.
5. **Alerts are DRAFT only**, HITL required, never CAP/OFFICIAL.
6. Data for the slice is a **SIMULATED** fixture on the Bogotá INTEGRATION CASE
   site. Deterministic runner: `python -m simulation.python.run --seed 42`.

## Alternatives

- Hydrodynamic 2D inundation — rejected for V1 (no DEM/calibration, would fake skill).
- Mixing exposure into PHI — rejected (hides the individual-first rule).
- Emitting OFFICIAL/CAP — rejected (no authority, HITL required).
- Labelling fixtures LIVE — rejected (honest evidence bar).

## Consequences

Horizon can colour catchments by operational risk with formula versions in the
popup. CHI, HCI engine, live adapters, and official alerting stay
NOT IMPLEMENTED. Thresholds are demo constants, not IDF curves.

## Validation

Pytest golden vectors for PHI/GCI; integration API tests; e2e fixture → API JSON;
seed-42 determinism.
