# ADR-0009 — Flood PHI rainfall + water-level merge (v0.2.0)

**Evidence:** IMPLEMENTED (formula + golden tests). Thresholds remain demo constants.

## Status

Accepted — 2026-10-01

## Context

IoT simulation delivers both `rainfall_mm` and `water_level_m` for the Bogotá
INTEGRATION CASE. V1 PHI used rainfall only (`flood.phi.rainfall-threshold.v0.1.0`).

## Decision

1. When a matching `water_level_m` observation exists for the same
   `spatial_unit_id`, PHI uses **`flood.phi.rainfall-hydro.v0.2.0`**.
2. Individual indices: rainfall thresholds (10/80 mm) and level thresholds
   (0.5/3.0 m demo).
3. **Merge rule:** `PHI = max(phi_rain, phi_hydro)` — conservative, not CHI.
4. Rainfall-only fixtures keep v0.1.0 behaviour via `compute_phi_with_hydro`
   when `water_level_m` is absent.

## Validation

`tests/unit/test_flood_phi_hydro.py`, IoT e2e asserts v0.2.0 when hydro present.
