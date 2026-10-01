# ADR-0011: Minimal CHI for flood + landslide rain coupling

**Status:** Accepted  
**Evidence:** IMPLEMENTED (`domains/compound/chi_flood_landslide.py`)

## Context

P2 adds a second individual hazard (landslide PHI, ADR-0010) alongside flood PHI (ADR-0006/0009). Some Colombia INTEGRATION CASE sites list both hazards on the same catchment or hillslope footprint. Operators need a **documented** compound index only when both individual PHIs are already elevated — not a hidden merge inside PHI.

## Physical justification

Intense short-duration rainfall simultaneously:

1. Raises fluvial / pluvial loading (flood PHI driver).
2. Increases pore pressure and reduces effective stress on slopes already predisposed by gradient and antecedent moisture (landslide PHI drivers in ADR-0010).

When **both** normalized PHIs exceed transparent screening gates, treat the shared rain driver as a **coupled exceedance** rather than assuming independence. This is a screening interaction term, not infinite-slope stability, not a calibrated debris-flow model, and **not** field-validated.

## Decision

Gate (both must hold at the same `spatial_unit_id` within a registered compound site):

- `phi_flood >= 0.25` (`FLOOD_PHI_MIN`)
- `phi_landslide >= 0.25` (`LANDSLIDE_PHI_MIN`)

Gates align with the lower “watch” band used in DRAFT alert mapping (~0.10–0.30 operational risk often corresponds to moderate PHI once E×V < 1).

When active:

```text
CHI = phi_flood + phi_landslide − phi_flood × phi_landslide
```

(`1 − (1−a)(1−b)` — conservative union for co-occurring rain-driven exceedance.)

When inactive: `CHI = 0` with `interaction_active = false` (individual-first).

`formula_version`: `compound.chi.flood-landslide-rain-coupling.v0.1.0`

## Alternatives considered

- `max(phi_flood, phi_landslide)` — rejected; duplicates individual-first policy, not compound.
- Un-gated product `phi_flood * phi_landslide` — rejected; amplifies noise when one hazard is negligible.

## Consequences

- Compound pairs configured under `configs/compound/` (site → flood + landslide fixture IDs).
- API: `GET /v1/compound/chi`.
- Does **not** replace operational risk or DRAFT alerts; CHI is an additional envelope for operator review.
- Not OFFICIAL alerting; human-in-the-loop unchanged.

## Validation

Unit tests with hand-computed values; integration test on `co-bogota-demo` SIMULATED pair.
