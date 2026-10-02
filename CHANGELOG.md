# Changelog

All notable changes to POLARIS are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning will follow SemVer once a tagged release exists.

## [Unreleased]

### Added

- **Product polish + local deploy:** `docker compose up --build` (PostGIS + API + Alembic on start), `make up` / `make down`, `docs/manuals/local-deployment.md`, complete `.env.example`, optional Mosquitto/NATS via compose profile `optional`
- **Horizon polish:** header with data_class badge, GCI legend, Vector link, optional OSM tiles via `POLARIS_MAP_TILE_ENABLED` / `POLARIS_MAP_TILE_URL` and `GET /v1/config/map`, optional landslide/wildfire overlay layers
- **Vector / Forge polish:** source-health stub, `fixture_id` URL sync with Horizon, scenario cards, `GET /v1/meta/demo-latest`, `harness/dev/smoke_compose.sh`
- **Horizon mobile:** WebView to configurable `/horizon/` URL; README for `flutter run` against local API

### Added

- **P5 release candidate prep:** `docs/manuals/technical-overview.md`, RF link budget `simulation/python/rf/` (FSPL **SIMULATED**), heat hazard registry stub, `make demo` / README reproducibility for `harness/demo/run_demo.sh`, draft workflow `release-response-quest.yml` for tag `v1.0.0-response-quest` (no tag until checklist + Helmut approval)

### Added (P0–P4 summary on main)

- **P4 wildfire baseline:** `wildfire.phi.fire-weather-pm.v0.1.0`, registry dispatch, SIMULATED `wildfire-co-bogota-demo`, ADR-0012
- **IoT fault injection:** scenario flags `fault_injection: packet_loss | gateway_down` for `simulation.python.iot_run`
- **Release manuals:** `docs/manuals/demo-script.md`, `docs/manuals/reproducibility-checklist-2026-10-08.md`

### Added

- **P3 Horizon Mobile (minimal):** Flutter `apps/horizon-mobile` — health + V1 assessments, map placeholder, offline cache stub; CI `flutter analyze` / `test` / `build apk --debug`
- **Forge studio shell:** static `apps/forge-studio` at `/forge/` — links to sim/replay/metrics
- **IEEE demo harness:** `harness/demo/run_demo.sh` + `run_demo.py` (test → sim-flood → API smoke log)
- **P2 minimal CHI:** `compound.chi.flood-landslide-rain-coupling.v0.1.0`, `GET /v1/compound/chi`, compound site pair `co-bogota-demo`, ADR-0011
- **Vector console (minimal):** static `apps/vector-console` at `/vector` — assessments, GCI/PHI/risk, CHI, DRAFT alerts, CAP link
- **CI PostGIS:** optional workflow job `pytest -m postgis` with PostGIS service container
- **P2 landslide baseline:** `landslide.phi.slope-moisture-rain.v0.1.0`, hazard registry dispatch, SIMULATED `landslide-co-slope-demo`, ADR-0010
- **CAP DRAFT/SIMULATION:** `schemas/alerts/cap-draft.json`, `GET /v1/alerts?format=cap` (JSON + XML Test status)
- **Site E/V v0.1:** configurable `exposure_vulnerability` in `configs/sites/*.yaml`, `risk.operational.phi-ev-site.v0.1.0` (EXPERIMENTAL)
- **P1 PostGIS persistence:** observation + assessment snapshot repository (SQLAlchemy/Alembic), compose PostGIS init, in-memory fallback, API `run_id` reads
- **LIVE_INTEGRATED Open-Meteo precipitation** for `co-bogota-demo` with stale-on-failure; `POST /v1/ingest/live/precipitation`; source catalog YAML
- **Flood PHI rainfall + hydro** `flood.phi.rainfall-hydro.v0.2.0` (ADR-0009)
- **SIMULATED IoT vertical slice:** weather + hydro virtual nodes → LoRa-ish comm → Pi 5 gateway (store-and-forward) → same V1 flood pipeline; `configs/devices/`, `python -m simulation.python.iot_run`, `POST /v1/ingest/iot`, ADR-0008, firmware stubs (PLACEHOLDER)
- **HISTORICAL_REPLAY** of the 31 Mar–1 Apr 2017 Mocoa event through the same V1 PHI/GCI/risk formulas, with hit/miss backtest (evidence **EXPERIMENTAL**, not HISTORICALLY_VALIDATED)
- `data_class=HISTORICAL_REPLAY` beside SIMULATED; LIVE still refused
- Runner `python -m harness.backtesting.replay --seed 42` and `GET /v1/backtests/flood-mocoa-2017-replay`
- Horizon `?fixture_id=flood-mocoa-2017-replay`
- ADR-0007
- `docs/product/obligaciones.md` (adapted project obligations snapshot)

### Added (V1, already on main)

- **V1 flood vertical slice** (SIMULATED Bogotá INTEGRATION CASE): observation → GCI → flood PHI baseline → operational risk (PHI × stub E/V) → DRAFT alert → API → Horizon MapLibre layer
- Versioned formulas: `gci.v0.1.0`, `flood.phi.rainfall-threshold.v0.1.0`, `risk.operational.phi-ev-stub.v0.1.0`, `alert.draft.v0.1.0`
- FastAPI routes: `/v1/observations`, `/v1/assessments`, `/v1/alerts`, `/v1/map/geojson` (plus `POST /v1/assessments/run`)
- Deterministic runner `python -m simulation.python.run --seed 42`
- ADR-0006 flood rainfall-threshold baseline
- Unit golden vectors (PHI, GCI, parsers), API integration tests, fixture→API e2e, seed-42 regression

### Changed

- `GET /health` maturity is now `P5-release-candidate-prep-2026-10-08`

### Changed (historical)

- `GET /health` maturity was `V1-flood-vertical-slice`
- Flood plugin evidence: PLACEHOLDER → IMPLEMENTED (rainfall-threshold PHI only)

### Security

- `.gitignore` excludes `.env` and dumps; `SECURITY.md` disclosure policy

## [0.0.1] — 2026-10-01 (P0 foundation)

### Added

- P0 engineering contract: README family, `MASTER_CURSOR_PROMPT.md`, `AGENTS.md`, `CONTRIBUTING.md`, ADRs, Apache-2.0 license
- Canonical modular-monolith directory tree with evidence-labelled READMEs
- FastAPI `GET /health` (**IMPLEMENTED**)
- JSON Schema envelopes for observation, hazard, risk, alert, and events
- CountryProfile stubs for 15 integration countries; Colombia Region + Site **INTEGRATION CASE**
- Hazard scaffold generator (`make scaffold-hazard`)
- Dev compose skeleton: Postgres/PostGIS, Mosquitto, NATS (**DESIGNED**, not production)
- GitHub Actions: Python ruff+pytest, C++ placeholder, path-filtered web/mobile, secret scan, release stub
- Cursor rules `00`–`14` and skills
