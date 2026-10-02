# Harness

**Evidence:** IMPLEMENTED — runnable entrypoints (not docs-only)

| Harness | Runner | Make |
|---------|--------|------|
| dev | `harness/dev/healthcheck.py` | `make health` |
| integration | `harness/integration/run_integration.py` | `make harness-integration` |
| simulation | `harness/simulation/run_simulation.py` | `make harness-simulation` |
| backtesting | `harness/backtesting/replay.py` | `make sim-replay` |
| fault-injection | `harness/fault-injection/run_faults.py` | `make harness-faults` |
| e2e | `harness/e2e/run_e2e.py` | `make harness-e2e` |
| demo | `harness/demo/run_demo.sh` | `make demo` |
| benchmark | `harness/benchmark/benchmark_flood.py` | `make harness-benchmark` |

Pytest suites under `tests/integration`, `tests/e2e`, and IoT fault unit tests complement these runners.
