# Changelog

All notable changes to POLARIS are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning will follow SemVer once a tagged release exists.

## [Unreleased]

### Added

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

- `GET /health` maturity is now `V1-flood-vertical-slice`
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
