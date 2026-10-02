# ADR-0013: Wildfire + landslide screening CHI

**Status:** Accepted  
**Evidence:** IMPLEMENTED (rule `wildfire-landslide-post-fire`, site `co-bogota-wildfire-landslide`)

## Context

Post-fire hillslopes can show co-elevated wildfire PHI (fire weather / PM) and landslide PHI (antecedent moisture + slope) on the same footprint. This is a **screening** interaction distinct from rain-only flood coupling (ADR-0011).

## Decision

- Rule `wildfire-landslide-post-fire` with gates `phi_wildfire >= 0.30`, `phi_landslide >= 0.25`.
- Union formula (ADR-0012 engine). `formula_version`: `compound.chi.wildfire-landslide-post-fire.v0.2.0`.
- Demo site overlaps `co-bogota-demo-center` SIMULATED fixtures; not burn-severity calibrated.

## Consequences

- Does not replace individual PHIs or operational risk.
- Not OFFICIAL alerting; human-in-the-loop unchanged.

## Validation

Unit test on rule load; integration test on registered site when center unit gates are met.
