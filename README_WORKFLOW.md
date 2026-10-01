# POLARIS workflow

**Evidence:** DESIGNED process · **IMPLEMENTED** as repo conventions (this file, CONTRIBUTING, CI, issue/PR templates).

## Branching

**Trunk-based.** `main` is always releasable at the current evidence bar (P0: contract + health + CI).

- Short-lived branches: `feature/*`, `fix/*`, `docs/*`
- Merge via PR. No long-lived release branches in this sprint (2026-10-01 → 2026-10-08).
- Do not dump unrelated history. Prefer one or few conventional commits per PR.

## Conventional Commits

```
<type>(<scope>): <summary>
```

Types: `feat`, `fix`, `docs`, `test`, `ci`, `chore`, `refactor`, `build`.

Scopes (examples): `repo`, `api`, `arch`, `sim`, `hazards`, `configs`, `ci`.

Examples:

- `feat(repo): P0 foundation scaffold and engineering contract`
- `fix(api): health payload includes evidence field`
- `docs(adr): record NATS as internal event bus`

## XP practices (adapted)

| Practice | How we apply it |
|----------|-----------------|
| Small slices | One vertical or one contract at a time; no mass codegen |
| Pair / agent+human | Agents follow `MASTER_CURSOR_PROMPT.md`; humans own merge |
| TDD where code exists | Health, generators, C++ placeholder have tests first or with the slice |
| Continuous integration | GitHub Actions on PR; `main` stays green |
| Collective ownership | CODEOWNERS are reviewers, not bottlenecks |

## CRISP-ML (research slices)

Hazard and index work after P0 follows CRISP-ML, not “train a model in the API”:

1. Business understanding (decision-support question)
2. Data understanding (catalog + licenses)
3. Data preparation (contracts, provenance)
4. Modeling (versioned formula or model card)
5. Evaluation (backtesting harness, baselines)
6. Deployment (only after evaluation artifacts exist)

Simulation engineering details: [README_SIMULATION_ENGINEERING.md](README_SIMULATION_ENGINEERING.md).

## Daily cadence (2026-10-01 – 2026-10-08)

| Day | Focus | Done when |
|-----|--------|-----------|
| 1 Oct | P0 contract + tree + CI | Draft PR, health green |
| 2 | P0 merge + schema freeze | `main` has foundation |
| 3 | First vertical start (one hazard interface, not full PHI) | Tests collect |
| 4 | Simulation fixture + determinism plan | Scenario YAML designed |
| 5 | API beyond health **only if** P0 merged | Versioned stub routes |
| 6 | Evidence pack for Response Quest (honest claims) | README maturity accurate |
| 7 | Hardening, disclaimers, demo script | No fake IMPLEMENTED |
| 8 | Release tag if CI green | 2026-10-08 |

Slippage: **cut scope**, do not fake features.

## Definition of Done (any PR)

- Evidence states updated (DESIGNED vs IMPLEMENTED)
- Tests or an explicit skip with path filter
- No secrets, no `.env`, no data dumps
- Conventional commit message
- Architecture impact noted if tree or ports change

## What not to do

- Commit generated business modules by the thousand
- Claim DESIGNED work as IMPLEMENTED
- Open PRs that mix firmware, Flutter UI, and PHI formulas
- Bypass human review for alerting copy
