# POLARIS architecture

**Evidence:** DESIGNED (system) · **P0 foundation IMPLEMENTED** · **V1 flood slice IMPLEMENTED** (GCI, flood PHI baseline, operational risk, DRAFT alerts, assessment API, Horizon GeoJSON map). CHI / HCI engine / live adapters remain NOT IMPLEMENTED.

This file is the **canonical scaffold**. Ignore inferred `packages/` + `sim/` trees from older gap notes.

## Style

POLARIS is a **modular monolith** with **hexagonal** (ports & adapters) and **clean architecture** boundaries.

- **Domain** never imports FastAPI, NATS, MQTT, PostGIS drivers, or UI kits.
- **Application** orchestrates use cases against ports.
- **Adapters** implement ports (storage, bus, IoT, national/global data).
- **Apps** are delivery: Horizon, Vector, Forge, mobile — thin clients of `platform/api`.

See [ADR-0001](docs/adr/0001-modular-monolith.md).

## Bounded contexts

| Context | Package | Responsibility |
|---------|---------|----------------|
| Territory | `domains/territory` | Country / Region / Site graphs and admin units |
| Observations | `domains/observations` | Typed sensor and source observations |
| Quality | `domains/quality` | Data quality and GCI (`gci.v0.1.0` IMPLEMENTED, minimal) |
| Hazards | `domains/hazards` + `hazards/*` | Per-phenomenon models (flood PHI baseline IMPLEMENTED; others PLACEHOLDER) |
| Compound | `domains/compound` | CHI interactions when evidence exists (NOT IMPLEMENTED) |
| Exposure | `domains/exposure` | People, assets, environment at risk (PLACEHOLDER stubs in V1) |
| Vulnerability | `domains/vulnerability` | Fragility and capacity (PLACEHOLDER stubs in V1) |
| Risk | `domains/risk` | Operational risk = PHI × E_stub × V_stub (IMPLEMENTED); CHI not mixed in |
| Alerting | `domains/alerting` | DRAFT decision-support messages; HITL required (IMPLEMENTED mapper) |
| Provenance | `domains/provenance` | `run_id`, formula versions, inputs, source IDs |

## Indices

| Index | Meaning | V1 evidence |
|-------|---------|-------------|
| **PHI** | Per-hazard individual index | IMPLEMENTED for flood rainfall-threshold baseline ([ADR-0006](docs/adr/0006-flood-phi-rainfall-baseline.md)) |
| **CHI** | Compound interaction index (only with evidence) | NOT IMPLEMENTED |
| **GCI** | Confidence / evidence quality | IMPLEMENTED (`gci.v0.1.0` minimal) |
| **HCI** | Operational output (alert level) — **never auto-evacuate** | DRAFT alert mapper IMPLEMENTED; HCI engine NOT IMPLEMENTED |

Principle: **individual-first, compound-second**. Do not mix phenomena without a documented interaction. Do not mix exposure into PHI.

## Territorial model

Configuration is hierarchical and versioned YAML (not live GIS in P0):

1. **CountryProfile** — ISO code, timezone, priority hazards, authorities (`configs/countries/`)
2. **RegionProfile** — nested under a country (`configs/regions/`)
3. **SiteProfile** — instrumented or modelled site (`configs/sites/`)

Fifteen **integration countries** have YAML stubs. They are **not pilots**. Colombia additionally has an example Region + Site labelled **INTEGRATION CASE**.

## Stack (DESIGNED)

| Layer | Choice | P0 |
|-------|--------|----|
| API | FastAPI | **IMPLEMENTED:** `GET /health` + V1 flood observation/assessment/alert/map |
| Geo DB | PostgreSQL + PostGIS | compose skeleton |
| Events | NATS ([ADR-0002](docs/adr/0002-nats-event-bus.md)) | compose skeleton |
| IoT telemetry | MQTT (Mosquitto) | compose skeleton |
| Web | Next.js / MapLibre (Horizon, Vector, Forge) | Horizon static MapLibre layer IMPLEMENTED; full Next apps DESIGNED |
| Mobile | Flutter ([ADR-0003](docs/adr/0003-flutter-mobile.md)) | README-only |
| Simulation | Python + C++20 + pybind11 + CMake ([ADR-0004](docs/adr/0004-python-cpp-simulator.md)) | placeholder lib + test |

Wokwi may appear later for MCU sketches. It is **not** the Digital Testbed. See [README_SIMULATION_ENGINEERING.md](README_SIMULATION_ENGINEERING.md).

## Canonical tree

```
apps/{horizon-web,vector-console,horizon-mobile,forge-studio}
platform/{domain,application,ports,adapters,api}
domains/{territory,observations,quality,hazards,compound,exposure,vulnerability,risk,alerting,provenance}
hazards/{common,flood,flash_flood,landslide,wildfire,drought,heat,cyclone,smoke,earthquake,tsunami,volcano,erosion_subsidence}
adapters/{data/global,data/national,iot,communications,storage,alerts}
configs/{countries,regions,sites,hazards,communications,devices}
simulation/{python,cpp,bindings,scenarios,fixtures,experiments,reports}
hardware/{requirements,reference-designs,schematics,pcb,bom,cad,enclosure,antenna,manufacturing}
firmware/{common,node,gateway,models}
data/{catalog,sample,synthetic}
backtesting/{datasets,events,baselines,experiments,reports}
schemas/{observation,hazard,risk,alerts,simulation,configuration}
harness/{dev,integration,simulation,backtesting,fault-injection,e2e,demo,benchmark}
generators/{hazard,source-adapter,country,site,sensor,communication,scenario}
docs/{adr,architecture,product,hazards,countries,sites,simulation,telecom,hardware,validation,security,manuals}
tests/{unit,integration,contract,property,e2e,regression}
infra/{docker,compose,monitoring,deployment}
.cursor/rules
.cursor/skills
.github/workflows
```

Do not recreate `packages/indices` or a top-level `sim/` as the home of the engine.

## Bootstrap order

Agents and humans must implement in this order. Skipping a layer to “just add a map” is scope creep.

1. **Schemas** — JSON Schema / OpenAPI contracts (`schemas/`)
2. **Configs** — Country → Region → Site → hazard flags
3. **Platform ports** — interfaces only
4. **Domain modules** — pure functions, versioned formulas
5. **Hazard plugins** — one phenomenon at a time via `generators/hazard`
6. **Adapters** — storage, bus, then external data
7. **API** — health, then versioned reads, then writes
8. **Simulation Digital Testbed** — deterministic scenarios before live IoT
9. **Harness / backtesting** — golden events
10. **Apps** — Horizon / Vector / Forge / mobile
11. **Firmware / hardware** — after contracts for payloads exist
12. **Communications / RF** — after device identity and provenance exist

## Alerting rules

- Every alert-shaped payload must carry provenance and a decision-support disclaimer.
- Human-in-the-loop is mandatory for HCI presentation.
- V1 emits **DRAFT** alerts only. CAP, SMS, and radio fan-out are **NOT IMPLEMENTED**.

## Physical / edge (DESIGNED)

Raspberry Pi edge station, MCU nodes, LoRa/MQTT gateways, enclosures, and BOM live under `hardware/` and `firmware/`. P0 contains directories and READMEs only.
