# POLARIS demo script (IEEE / release freeze)

**Evidence:** IMPLEMENTED (manual)  
**Target freeze:** 2026-10-08  
**Data class:** SIMULATED and HISTORICAL_REPLAY only — never present outputs as OFFICIAL or LIVE evacuation orders.

## Prerequisites

- Python ≥ 3.12, `pip install -e ".[dev]"`
- Optional: Docker for PostGIS compose (API falls back to in-memory storage)

## 1. Health and maturity

```bash
make health
```

Expect `status=ok`, `maturity=P4-wildfire-fault-release-prep-2026-10-08`, disclaimer in API responses elsewhere.

## 2. Automated gate (CI parity)

```bash
make lint
make test
```

## 3. Flood SIMULATED slice

```bash
make sim-flood
python -m simulation.python.run --seed 42
```

Open Horizon: `make api` → http://127.0.0.1:8000/horizon/

## 4. Historical replay (EXPERIMENTAL)

```bash
make sim-replay
curl -s "http://127.0.0.1:8000/v1/backtests/flood-mocoa-2017-replay?seed=42" | head
```

State clearly: **EXPERIMENTAL**, not HISTORICALLY_VALIDATED.

## 5. Landslide + wildfire baselines

```bash
curl -s "http://127.0.0.1:8000/v1/assessments?fixture_id=landslide-co-slope-demo&seed=42" | jq '.assessments[0].phi.formula_version'
curl -s "http://127.0.0.1:8000/v1/assessments?fixture_id=wildfire-co-bogota-demo&seed=42" | jq '.assessments[0].phi.formula_version'
```

## 6. SIMULATED IoT + fault injection

```bash
python -m simulation.python.iot_run --scenario simulation/scenarios/iot-bogota-demo.yaml --seed 42
python -m simulation.python.iot_run --scenario simulation/scenarios/iot-bogota-fault-packet-loss.yaml --seed 42
python -m simulation.python.iot_run --scenario simulation/scenarios/iot-bogota-fault-gateway-down.yaml --seed 42
```

Explain store-and-forward when `fault_injection: gateway_down`.

## 7. Compound CHI (minimal)

```bash
curl -s "http://127.0.0.1:8000/v1/compound/chi?site_id=co-bogota-demo&seed=42" | jq '.chi.value'
```

## 8. DRAFT alerts only

```bash
curl -s "http://127.0.0.1:8000/v1/alerts?seed=42" | jq '.alerts[0].status'
curl -s "http://127.0.0.1:8000/v1/alerts?format=cap&seed=42" | head
```

CAP output is **DRAFT/SIMULATION** XML/JSON — not OFFICIAL CAP fan-out.

## 9. Surfaces

- `/vector/` — operator console (static)
- `/forge/` — studio shell links
- Horizon Mobile — debug APK via CI (`apps/horizon-mobile`); not app-store release

## Closing line for audience

POLARIS supports human-in-the-loop decision research. Operators must review every DRAFT alert before any operational action.
