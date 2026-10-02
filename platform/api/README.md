# platform/api

**Evidence:** IMPLEMENTED health + V1 flood slice routes

FastAPI delivery.

| Path | Evidence |
|------|----------|
| `GET /health` | IMPLEMENTED |
| `GET /v1/observations` | IMPLEMENTED (SIMULATED or HISTORICAL_REPLAY) |
| `GET /v1/assessments` | IMPLEMENTED |
| `POST /v1/assessments/run` | IMPLEMENTED |
| `GET /v1/alerts` | IMPLEMENTED (DRAFT only) |
| `GET /v1/map/geojson` | IMPLEMENTED |
| `GET /v1/mobile/bootstrap` | IMPLEMENTED (maturity, fixtures, Horizon path) |
| `GET /v1/config/map` | IMPLEMENTED (Horizon tile env) |
| `GET /v1/meta/demo-latest` | IMPLEMENTED (latest demo log path) |
| `GET /v1/backtests/{scenario_id}` | IMPLEMENTED (HISTORICAL_REPLAY, EXPERIMENTAL) |
| `GET /horizon/` | IMPLEMENTED static mount of `apps/horizon-web` |
| `GET /vector/` | IMPLEMENTED static mount of `apps/vector-console` |
| `GET /forge/` | IMPLEMENTED static mount of `apps/forge-studio` |

No LIVE adapters. No OFFICIAL alerts. Domain math is not in the router.
