# infra/compose

**Evidence:** IMPLEMENTED (local demo) — PostGIS init, API Dockerfile, optional MQTT/NATS.

| Asset | Role |
|-------|------|
| `postgres-init.sql` | PostGIS extension on first boot |
| `Dockerfile.api` | Python 3.12 image with POLARIS package |
| `api-entrypoint.sh` | Wait for Postgres → Alembic → uvicorn |
| `mosquitto.conf` | Optional profile `optional` |
| `compose.yml` | Label overlay for `docker compose config` |

Primary entry: repo-root `docker-compose.yml`. See [docs/manuals/local-deployment.md](../../docs/manuals/local-deployment.md).

**Not production** — no HA, backups, or exposure to the public internet.
