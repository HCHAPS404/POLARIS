# POLARIS

**Evidence:** DESIGNED (product + architecture) · **P0 foundation IMPLEMENTED** (contract, canonical tree, CI guardrails, `GET /health`). Hazard models, maps, IoT, RF, energy, Flutter/Next apps, live adapters, and CAP alerting are **NOT IMPLEMENTED**.

**POLARIS** (adaptive multi-hazard intelligence architecture) is a **decision-support** system. It is **not** an official evacuation authority. Humans remain in the loop. Alerts without provenance and disclaimer are forbidden.

| Field | Value |
|-------|--------|
| Competition | IEEE Response Quest 2026 |
| Team | Helmut, Laura, Lenin |
| Target release (this sprint) | 2026-10-08 |
| License | Apache-2.0 ([ADR-0005](docs/adr/0005-apache-2.0-license.md)) |
| Repo maturity | Foundation on `main` once this PR merges; previously a 27-byte stub |

## Products (DESIGNED)

| Product | Surface | Role | P0 status |
|---------|---------|------|-----------|
| **Horizon** | `apps/horizon-web` | Institutional / operations dashboard (web) | README + directory only |
| **Vector** | `apps/vector-console` | Operator console and field coordination | README + directory only |
| **Forge** | `apps/forge-studio` | Model, scenario, and configuration studio | README + directory only |
| Horizon Mobile | `apps/horizon-mobile` | Flutter field app ([ADR-0003](docs/adr/0003-flutter-mobile.md)) | README + directory only |

## What this repository is today

P0 establishes the **engineering contract in git**: architecture, workflow, simulation rules, agent instructions, ADRs, schemas, country config stubs, a FastAPI health endpoint, and CI that can go green on `main`.

It does **not** compute PHI / CHI / GCI / HCI, ingest live data, drive maps, or emit operational alerts.

## Engineering contract (read in this order)

1. [MASTER_CURSOR_PROMPT.md](MASTER_CURSOR_PROMPT.md) — agent priorities P0–P6
2. [README_ARCHITECTURE.md](README_ARCHITECTURE.md) — modular monolith, hexagonal + clean, canonical tree
3. [README_WORKFLOW.md](README_WORKFLOW.md) — trunk-based, conventional commits, XP, CRISP-ML, daily 2026-10-01…08
4. [README_SIMULATION_ENGINEERING.md](README_SIMULATION_ENGINEERING.md) — Digital Testbed (Python / C++20 / pybind11); Wokwi is **not** primary
5. [AGENTS.md](AGENTS.md) · [CONTRIBUTING.md](CONTRIBUTING.md) · [CODEOWNERS](CODEOWNERS)

## Quickstart (what actually runs)

Requires Python **≥ 3.12**.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
make health          # GET /health via FastAPI TestClient / uvicorn check
make test            # pytest (health + scaffold collection)
make lint            # ruff
make scaffold-hazard NAME=demo_hazard
```

Dev compose (Postgres/PostGIS, Mosquitto, NATS) is a **DESIGNED skeleton**, not production:

```bash
docker compose -f docker-compose.yml -f infra/compose/compose.yml config
```

## Evidence legend

| State | Meaning |
|-------|---------|
| **IMPLEMENTED** | Code exists, tests or a runnable check exist, CI can exercise it |
| **DESIGNED** | Specified in architecture/config; no working domain implementation |
| **PLACEHOLDER** | Directory, README, empty module, or stub interface only |
| **NOT IMPLEMENTED** | Explicitly out of the current phase |

**Current maturity:** DESIGNED product · **foundation IMPLEMENTED** (tree + contract + health + CI).

## Legal / operational disclaimer

POLARIS supports situational awareness and research. It does **not** replace UNGRD, USGS, JMA, or any national warning service. Do not present simulated or prototype outputs as official warnings.

## Team

| Person | Focus (working assignment) |
|--------|----------------------------|
| Helmut | Architecture, platform, simulation kernel |
| Laura | Product surfaces (Horizon / Vector / Forge), UX, documentation |
| Lenin | Hazards, territorial configs, GIS/data research |

## License

Apache License 2.0. See [LICENSE](LICENSE) and [ADR-0005](docs/adr/0005-apache-2.0-license.md).
