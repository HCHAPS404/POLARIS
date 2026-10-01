# platform/api

**Evidence:** IMPLEMENTED health + V1 flood slice routes

FastAPI delivery.

| Path | Evidence |
|------|----------|
| `GET /health` | IMPLEMENTED |
| `GET /v1/observations` | IMPLEMENTED (SIMULATED fixture) |
| `GET /v1/assessments` | IMPLEMENTED |
| `POST /v1/assessments/run` | IMPLEMENTED |
| `GET /v1/alerts` | IMPLEMENTED (DRAFT only) |
| `GET /v1/map/geojson` | IMPLEMENTED |
| `GET /horizon/` | IMPLEMENTED static mount of `apps/horizon-web` |

No LIVE adapters. No OFFICIAL alerts. Domain math is not in the router.
