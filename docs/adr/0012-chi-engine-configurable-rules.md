# ADR-0012: CHI engine v0.2 — configurable compound rules

**Status:** Accepted  
**Evidence:** IMPLEMENTED (`domains/compound/chi_engine.py`, `configs/compound/rules/`)

## Context

ADR-0011 hard-coded flood + landslide gates and the union formula in Python constants. Forge and backtesting need **traceable rule IDs**, versioned formula strings, and room for additional justified pairs without forked code paths.

## Decision

- Store rules as YAML under `configs/compound/rules/` (`rule_id`, `hazard_ids`, `phi_min`, `formula`, versions).
- Evaluate via `chi_engine.evaluate_chi` / `build_chi_record` (v0.2 model version family).
- Site registry references `rule_id` and ordered hazard/fixture pairs (`configs/compound/*.yaml`).
- Supported formula in v0.2: `union` only (same as ADR-0011).

## Consequences

- `chi_flood_landslide.py` remains a compatibility wrapper for tests and docs.
- API compound payloads include `rule_id` and generic `phi_{hazard}` fields.
- Adding a pair requires ADR justification + rule file + site config + tests.

## Validation

Unit tests on rule loading, gate behaviour, and Bogotá compound integration paths.
