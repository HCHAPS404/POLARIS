# POLARIS — Technical overview (evidence table)

**Evidence:** IMPLEMENTED (documentation)  
**Release target:** 2026-10-08 response-quest RC  
**Tag (draft only):** `v1.0.0-response-quest` — do **not** push until [reproducibility checklist](reproducibility-checklist-2026-10-08.md) passes and Helmut approves.

POLARIS is **decision-support only**. Humans in the loop. No OFFICIAL evacuation authority.

## Legend

| Label | Meaning |
|-------|---------|
| **IMPLEMENTED** | Runnable code + tests or CI job |
| **SIMULATED** | Deterministic or seeded synthetic data; never LIVE/OFFICIAL |
| **EXPERIMENTAL** | Runnable but not validated for operations |
| **DESIGNED** | Spec / skeleton only |
| **PLACEHOLDER** | Stub interface or registry entry |
| **NOT IMPLEMENTED** | Explicitly out of scope for this RC |

## Platform and delivery

| Area | Evidence | Notes |
|------|----------|-------|
| `GET /health` | IMPLEMENTED | Maturity `P5-release-candidate-prep-2026-10-08` |
| FastAPI V1 observations/assessments/alerts/map | IMPLEMENTED | SIMULATED + HISTORICAL_REPLAY fixtures |
| PostGIS persistence | IMPLEMENTED | Optional; in-memory fallback |
| CAP OFFICIAL alerting | NOT IMPLEMENTED | DRAFT/SIMULATION via `format=cap` only |
| Compose (Postgres/MQTT/NATS) | DESIGNED | Dev skeleton |

## Hazards (PHI baselines)

| Hazard | Registry | PHI / slice | Data class |
|--------|----------|-------------|------------|
| Flood | IMPLEMENTED | `flood.phi.rainfall-threshold.v0.1.0` (+ hydro merge) | SIMULATED |
| Landslide | IMPLEMENTED | `landslide.phi.slope-moisture-rain.v0.1.0` | SIMULATED |
| Wildfire | IMPLEMENTED | `wildfire.phi.fire-weather-pm.v0.1.0` | SIMULATED |
| Heat | PLACEHOLDER | No runner | — |
| Compound CHI flood+landslide | IMPLEMENTED | `compound.chi.flood-landslide-rain-coupling.v0.1.0` | SIMULATED |

## Simulation and IoT

| Component | Evidence | Notes |
|-----------|----------|-------|
| `simulation.python.run` | IMPLEMENTED | Seeded flood / multi-hazard fixtures |
| `simulation.python.iot_run` | IMPLEMENTED | SIMULATED sensors → LoRa-ish comm → gateway |
| IoT fault injection | IMPLEMENTED | `packet_loss`, `gateway_down` scenarios |
| RF FSPL / link budget | IMPLEMENTED **SIMULATED** | `simulation/python/rf/` |
| C++ kernel | PLACEHOLDER | CI placeholder job |

## Data and adapters

| Source | Evidence | Notes |
|--------|----------|-------|
| Synthetic fixtures | IMPLEMENTED | `data/synthetic/*.simulated.json` |
| Mocoa 2017 replay | IMPLEMENTED **EXPERIMENTAL** | Not HISTORICALLY_VALIDATED |
| Open-Meteo precipitation | IMPLEMENTED | LIVE_INTEGRATED with stale-on-failure |

## Apps

| App | Evidence | Notes |
|-----|----------|-------|
| Horizon Web | IMPLEMENTED | MapLibre V1 GeoJSON |
| Vector console | IMPLEMENTED | Static operator shell |
| Forge studio | IMPLEMENTED | Static links to sim/replay |
| Horizon Mobile | IMPLEMENTED | Flutter analyze/test/debug APK in CI |

## Reproducibility entrypoints

| Step | Command |
|------|---------|
| Full demo harness | `./harness/demo/run_demo.sh` |
| Manual checklist | [reproducibility-checklist-2026-10-08.md](reproducibility-checklist-2026-10-08.md) |
| Demo narrative | [demo-script.md](demo-script.md) |

## Out of scope for this RC

Territorial graphs (P5 roadmap), PCB KiCad, live RF measurements, energy domain, full HCI engine, app-store mobile release, competition submission tag without Helmut sign-off.
