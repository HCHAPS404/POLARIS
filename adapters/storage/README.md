# adapters/storage

**Evidence:** IMPLEMENTED

| Component | Evidence |
|-----------|----------|
| SIMULATED / HISTORICAL_REPLAY fixtures | IMPLEMENTED (`simulated_json.py`) |
| In-memory repository | IMPLEMENTED (default when no DB) |
| PostGIS + SQLAlchemy | IMPLEMENTED (local dev; Alembic migrations) |
| LIVE fixture loader | Refuses `data_class=LIVE` (not faked) |

**Limitations:** No HA, no spatial queries on geometry (JSONB payload only), no production backup story. Integration tests gated by `@pytest.mark.postgis` and `POLARIS_DATABASE_URL`.

**Dev:** `make db-up` · `make db-migrate` · see `.env.example`.
