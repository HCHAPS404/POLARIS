# MASTER_CURSOR_PROMPT — POLARIS

**Evidence:** IMPLEMENTED as the agent contract for this repository. Product capabilities described below remain DESIGNED unless a later PR marks them IMPLEMENTED.

You are working on **POLARIS**, IEEE Response Quest 2026, team **Helmut, Laura, Lenin**, target **2026-10-08**.

Read first: `README.md`, `README_ARCHITECTURE.md`, `README_WORKFLOW.md`, `README_SIMULATION_ENGINEERING.md`, `AGENTS.md`. Follow `.cursor/rules` (especially `00-polaris-core.mdc`). Invoke `.cursor/skills` when the task matches.

## Identity

POLARIS is **decision-support**, not an official warning service. Human-in-the-loop. No fake claims. DESIGNED ≠ IMPLEMENTED.

Canonical tree is the modular monolith in `README_ARCHITECTURE.md`. **Do not** create `packages/` or a top-level `sim/` as the engine home.

## Priority scale (official)

| Level | Meaning | Status at P0 merge |
|-------|---------|--------------------|
| **P0** | Repo foundation: contract files, canonical empty tree, ADRs, CI guardrails, health, schemas, country stubs, generators, compose skeleton | **merged-or-stacked base** |
| **P1** | Data contracts beyond envelopes: OpenAPI growth, catalog, migrations stubs | V1 extended observation/assessment/alert schemas |
| **P2** | Mathematical engine: normalization + PHI for **one** hazard, versioned tests | **V1 flood PHI + GCI IMPLEMENTED** |
| **P3** | Deterministic Digital Testbed runner (`polaris sim run`), seeds, golden JSON | **narrow IMPLEMENTED** (flood demo + Mocoa 2017 HISTORICAL_REPLAY); full testbed DESIGNED |
| **P4** | Backend vertical: PostGIS optional, one index/alert read path, compose actually used | **in-memory SIMULATED path IMPLEMENTED**; PostGIS still DESIGNED |
| **P5** | Territorial graphs in memory or PostGIS | not started (V1 uses 3 GeoJSON polygons) |
| **P6** | Horizon/Vector/Forge apps, Flutter, IoT/firmware, RF, hardware, MLOps | **Horizon map layer IMPLEMENTED** (static); remaining P6 NOT IMPLEMENTED |

P0 forbids PHI/CHI/GCI engines, maps, IoT, RF, energy, Flutter app, Next.js apps, live adapters, and CAP logic **unless the user explicitly requests a later slice**. V1 is that explicit flood slice.

## Operating rules

1. Update evidence headers on every module you touch.
2. Prefer editing architecture docs over inventing parallel trees.
3. Use `make scaffold-hazard NAME=...` instead of hand-copying hazard packages.
4. Never commit secrets, credentials, or `.env`.
5. Never emit alert UX without disclaimer + provenance fields in the schema.
6. Conventional Commits. Small PRs.
7. If a job (Flutter, pnpm) has no app manifest, skip it — do not fail `main`.
8. Spanish or English docs are fine; code identifiers stay English.

## Bootstrap order

Schemas → configs → ports → domain → hazard plugins → adapters → API → simulation → harness → apps → firmware/hardware → RF.

## Definition of done for agent work

- Tests or a documented skip
- CI still meaningful
- README claims match git
- No mass-generated business code
