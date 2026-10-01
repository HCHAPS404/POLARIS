# AGENTS.md

**Evidence:** IMPLEMENTED (agent operating manual for this repo).

Instructions for Cursor agents and humans pairing with them. Nested `AGENTS.md` files exist only in `simulation/`, `hazards/`, `hardware/`, and `apps/horizon-mobile/`.

## Always

1. Treat `README_ARCHITECTURE.md` as the tree and layering source of truth.
2. Treat `MASTER_CURSOR_PROMPT.md` as priority and scope control (P0–P6).
3. Apply `.cursor/rules/00-polaris-core.mdc` on every task.
4. Load a skill from `.cursor/skills/<name>/SKILL.md` when the work matches (architecture, backend, hazard-model, simulation, cpp, …).
5. Mark evidence: IMPLEMENTED / DESIGNED / PLACEHOLDER / NOT IMPLEMENTED.
6. POLARIS is not Shopify Polaris, not a CSS kit, not an ocean-buoy product (HEXA/VYDRA).

## Never

- Implement CHI, live adapters, RF, energy, Flutter UI, or CAP in a P0-scoped task. The V1 flood slice (SIMULATED PHI/GCI/DRAFT) is in-tree; do not expand it into those areas unasked.
- Paste entire README files into Cursor rules.
- Claim DESIGNED as IMPLEMENTED.
- Add `packages/` or replace `simulation/` with a Wokwi-first story.
- Commit `.env`, keys, dumps, or `node_modules`.
- Auto-send operational alerts.

## Tooling

- Python ≥ 3.12: `make test`, `make lint`, `make health`, `make sim-flood`, `make api`
- C++20: `make test-cpp` (placeholder)
- Scaffold: `make scaffold-hazard NAME=flood`
- Compose: design-only skeleton in `docker-compose.yml` and `infra/compose/`

## Review bar

A change is mergeable when CI Python (ruff + pytest on what exists) is green, secret scan is clean, and the PR states architecture impact and evidence honestly.
