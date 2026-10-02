# Local deployment (Docker)

**Evidence:** IMPLEMENTED — one-command demo stack for PostGIS + API + static Horizon/Vector/Forge.

POLARIS is **decision-support only**. No OFFICIAL alerts. Data on the map is `SIMULATED` or `HISTORICAL_REPLAY` unless explicitly documented otherwise.

## Prerequisites

- Docker Engine 24+ and Docker Compose v2
- Git clone of this repository (recommended checkout for the pre-local bundle: **`v1.1.0-pre-local`** when the tag is published on `main`)

```bash
git fetch --tags
git checkout v1.1.0-pre-local   # optional; main may match pre-local maturity string in GET /health
```
- Optional: Flutter SDK 3.24+ if you build the Horizon Mobile APK (`apps/horizon-mobile`)
- Optional: outbound HTTPS if you enable OSM raster tiles (`POLARIS_MAP_TILE_ENABLED=1`)

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

Makefile shortcuts:

```bash
make up      # docker compose up --build -d
make down    # docker compose down
```

Wait until the API container logs `Application startup complete`, then verify:

| URL | Purpose |
|-----|---------|
| http://localhost:8000/health | Liveness + storage backend |
| http://localhost:8000/docs | OpenAPI |
| http://localhost:8000/horizon/ | MapLibre flood slice |
| http://localhost:8000/vector/ | Operator console |
| http://localhost:8000/forge/ | Scenario studio cards |

## Seed / demo data

Fixtures ship in `data/synthetic/` — no separate DB seed is required for the map.

### Harness (post-backlog `main`)

| Command | Scope |
|---------|--------|
| `make harness-e2e` | **Ola 2 chain:** sim flood + IoT → pytest `tests/e2e` → API smoke (no Docker) |
| `python harness/e2e/run_e2e.py --postgis` | Same + PostGIS roundtrip when `POLARIS_DATABASE_URL` is set |
| `make demo` | Full IEEE bundle: **all** pytest + sim-flood + API smoke log |
| `make demo-compose` / `docker compose exec api make demo` | Demo inside running stack |

See [harness/e2e/README.md](../../harness/e2e/README.md).

Logs land in `harness/demo/output/demo-*.log` when you run `make demo` locally.

## PostGIS migrations

On API container start, `infra/compose/api-entrypoint.sh` waits for PostgreSQL, then runs:

`alembic upgrade head`

If the API exits during boot, check Postgres health (`docker compose ps`) and that port `5432` is free on the host.

## Optional services

MQTT (Mosquitto) and NATS are **not** required for the MVP demo. Enable them with:

```bash
docker compose --profile optional up --build
```

See `infra/compose/README.md` for ports.

## Map tiles (Horizon)

Default: local background only (no external tile fetch).

To use OpenStreetMap raster tiles:

```env
POLARIS_MAP_TILE_ENABLED=1
# optional override:
# POLARIS_MAP_TILE_URL=https://tile.openstreetmap.org/{z}/{x}/{y}.png
```

Horizon also exposes a runtime toggle when the API reports tiles as enabled.

## Host-only development (without API container)

```bash
make db-up
export POLARIS_DATABASE_URL=postgresql+psycopg://polaris:polaris@localhost:5432/polaris
make db-migrate
make api
```

Use `.env.example` localhost URL variants when running uvicorn on the host.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `port is already allocated` | Change `API_PORT` / `POSTGRES_PORT` in `.env` |
| API stuck on “Waiting for PostgreSQL” | Ensure `postgres` service is healthy; first boot can take ~30s for PostGIS init |
| Horizon “Cannot load assessments” | Confirm `curl -s localhost:8000/health` returns `"status":"ok"` |
| Storage shows `memory` inside compose | Check `POLARIS_DATABASE_URL` points at `@postgres:5432`, not `@localhost` |
| OSM tiles blank | Enable `POLARIS_MAP_TILE_ENABLED=1` and allow HTTPS egress; respect OSM tile usage policy |

## Smoke script

```bash
make smoke-compose
```

Runs `harness/dev/smoke_compose.sh` (curl health + geojson). Optional in CI.
