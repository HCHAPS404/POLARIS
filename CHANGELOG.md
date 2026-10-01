# Changelog

All notable changes to POLARIS are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning will follow SemVer once a tagged release exists.

## [Unreleased]

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

### Security

- `.gitignore` excludes `.env` and dumps; `SECURITY.md` disclosure policy
