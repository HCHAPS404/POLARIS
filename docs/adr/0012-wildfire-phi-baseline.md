# ADR-0012: Wildfire PHI fire-weather-pm baseline (P4)

- **Status:** Accepted
- **Date:** 2026-10-01
- **Evidence:** IMPLEMENTED (`hazards/wildfire/phi.py`, SIMULATED fixture `wildfire-co-bogota-demo`)

## Context

POLARIS needs a third individual-first hazard plugin after flood and landslide, without claiming NFDRS/FWI calibration or official fire warnings.

## Decision

Implement `wildfire.phi.fire-weather-pm.v0.1.0`:

- Susceptibility from normalized temperature, inverted relative humidity, and wind speed (equal-weight mean).
- Optional detection term from PM2.5 when observations exist.
- PHI = max(susceptibility, detection). Exposure/vulnerability excluded from PHI.

## Alternatives

- Full fuel-moisture and terrain models — rejected for P4 scope.
- PM-only smoke hazard — rejected; wildfire plugin owns fire-weather + optional PM.

## Consequences

- Registry and `run_hazard_slice` dispatch include `wildfire`.
- Observation parser accepts fire-weather and PM properties on SIMULATED fixtures.

## Validation

- `tests/unit/hazards/test_wildfire_phi.py`
- `tests/unit/test_wildfire_slice.py`
- CI ruff + pytest
