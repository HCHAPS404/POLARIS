# harness/e2e

**Evidence:** IMPLEMENTED — one script exercises simulation → pytest e2e → API smoke → optional PostGIS.

## Runner

```bash
make harness-e2e
# or:
python harness/e2e/run_e2e.py
```

### What runs (default)

1. **Digital Testbed** — `simulation.python.run` (flood Bogotá demo, seed 42)
2. **IoT SIMULATED pipeline** — `simulation.python.iot_run` (Bogotá demo)
3. **Pytest e2e** — `tests/e2e/` (fixture → domain → FastAPI JSON, replay, backtest experiments)
4. **API smoke** — `harness/demo/run_demo.py` (TestClient, no open port)

### Optional PostGIS

With Postgres/PostGIS up and migrations applied:

```bash
export POLARIS_DATABASE_URL=postgresql+psycopg://polaris:polaris@localhost:5432/polaris
make db-migrate
python harness/e2e/run_e2e.py --postgis
```

Or rely on auto-detection when `POLARIS_DATABASE_URL` is set (same flag behavior as integration harness).

### Flags

| Flag | Effect |
|------|--------|
| `--skip-sim` | Pytest e2e + API smoke only |
| `--postgis` | Append `tests/integration -m postgis` |
| `--seed N` | Override deterministic seed (default 42) |

## Related

| Harness | Purpose |
|---------|---------|
| `make demo` | Full IEEE bundle: **all** pytest + sim-flood + API smoke (see `harness/demo/`) |
| `make harness-integration` | API integration pytest (skips postgis by default) |
| `make smoke-compose` | Live stack curl smoke after `docker compose up` |

Do **not** claim competition submission or global HISTORICALLY_VALIDATED from harness logs alone.
