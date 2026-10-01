# POLARIS simulation engineering

**Evidence:** DESIGNED (Digital Testbed) · **P0 PLACEHOLDER IMPLEMENTED** (C++20 lib + test, Python package layout, scenarios directory). No hazard physics in this phase.

## Digital Testbed (primary)

The primary simulation environment is a **reproducible Digital Testbed** in this monorepo:

| Layer | Path | Role |
|-------|------|------|
| Python orchestration | `simulation/python` | Scenarios, seeds, reports, fixtures |
| C++20 kernel | `simulation/cpp` | Numerical kernels (placeholder `add` in P0) |
| Bindings | `simulation/bindings` | pybind11 (DESIGNED; not wired in P0) |
| Scenarios | `simulation/scenarios` | YAML scene definitions |
| Fixtures | `simulation/fixtures` | Golden inputs |
| Experiments | `simulation/experiments` | Run manifests |
| Reports | `simulation/reports` | Generated artifacts (gitignored dumps) |

Build: root [CMakeLists.txt](CMakeLists.txt) (C++20). Orchestrate with `make test-cpp` when a compiler is available.

Contract: [ADR-0004](docs/adr/0004-python-cpp-simulator.md).

## Wokwi is not primary

[Wokwi](https://wokwi.com) may be used later to **sketch** MCU firmware (`firmware/`). It is:

- **not** the source of truth for hazard models
- **not** the Digital Testbed
- **not** an acceptable substitute for seeded Python/C++ scenarios

Do not generate POLARIS “simulations” as Wokwi wiring diagrams.

## Determinism rules (binding from P1 onward)

When a runner exists it **must**:

1. Accept `--seed` (integer)
2. Record `formula_version`, `schema_version`, `git_sha`, `run_id`
3. Same seed + same fixtures → same JSON (bit-stable or documented tolerance)
4. Refuse wall-clock as a model input unless injected as a scenario parameter

P0 has **no** `polaris sim run` CLI. Do not claim otherwise.

## Fault injection and backtesting

Harnesses live under `harness/simulation`, `harness/fault-injection`, and `backtesting/`.
`python -m harness.backtesting.replay --seed 42` is IMPLEMENTED for Mocoa 2017
(HISTORICAL_REPLAY, evidence EXPERIMENTAL). Fault injection remains PLACEHOLDER.

## Agent rules

- Prefer tiny, tested kernels over notebooks that cannot rerun.
- Never silently fall back to random unseeded draws in tests.
- Provenance metadata is mandatory for any generated scenario or scaffold (`generators/`).
