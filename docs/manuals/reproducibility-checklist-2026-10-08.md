# Reproducibility checklist — release 2026-10-08

**Evidence:** IMPLEMENTED (checklist)  
**Branch target:** `main` after P5 RC merge (PR #10)

| Step | Command / check | Expected |
|------|-----------------|----------|
| 1 | `git rev-parse HEAD` | Record SHA in release notes |
| 2 | `pip install -e ".[dev]"` | Clean venv |
| 3 | `make lint` | Ruff clean |
| 4 | `make test` | All pytest green (incl. e2e, optional postgis skipped locally) |
| 5 | `make health` | HTTP 200, maturity `P5-release-candidate-prep-2026-10-08` |
| 4b | `./harness/demo/run_demo.sh` or `make demo` | Log under `harness/demo/output/` |
| 4c | `pytest tests/unit/test_rf_fspl.py` | FSPL SIMULATED link budget |
| 6 | `make sim-flood` | Deterministic JSON, seed 42 |
| 7 | `python -m simulation.python.iot_run --seed 42` | 2 packets, DRAFT flood assessment |
| 8 | `python -m simulation.python.iot_run --scenario simulation/scenarios/iot-bogota-fault-gateway-down.yaml --seed 42` | `fault_injection=gateway_down`, store-and-forward |
| 9 | `curl localhost:8000/v1/assessments?fixture_id=wildfire-co-bogota-demo&seed=42` | `wildfire.phi.fire-weather-pm.v0.1.0` |
| 10 | Secret scan / CI | No keys in git (`.env` not committed) |
| 11 | Disclaimer | No OFFICIAL CAP; alerts remain DRAFT |

Sign-off: Helmut approves tag `v1.0.0-response-quest` — do **not** claim competition submission complete before that. Operator confirms demo used SIMULATED/HISTORICAL_REPLAY labels only.
