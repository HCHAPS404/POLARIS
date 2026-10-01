# ADR-0010: Landslide PHI slope-moisture-rain baseline

**Status:** Accepted  
**Evidence:** IMPLEMENTED (`hazards/landslide/phi.py`)

## Context

P2 requires a second hazard in the same pipeline (observation → GCI → PHI → risk → DRAFT) without claiming field validation.

## Decision

Use transparent normalized factors:

- Slope and soil moisture define a static susceptibility average.
- 1h rainfall defines a trigger index.
- PHI = max(susceptibility, trigger) (conservative, individual-first).

`formula_version`: `landslide.phi.slope-moisture-rain.v0.1.0`

## Limitations

No pore pressure, no antecedent rain, not calibrated to Colombian inventories, not HISTORICALLY_VALIDATED.

## Consequences

Registry entry in `domains/hazards/registry.py`; SIMULATED fixture `landslide-co-slope-demo`.
