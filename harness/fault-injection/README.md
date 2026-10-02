# harness/fault-injection

**Evidence:** IMPLEMENTED (SIMULATED IoT fault scenarios + importable runner)

Legacy IoT scenarios with `gateway_down` and `packet_loss` fault flags:

```bash
python harness/fault-injection/run_faults.py
make harness-faults
```

Unit coverage: `tests/unit/test_iot_fault_injection.py`.

Forge-style catalogue runner (`harness/fault_injection/`):

```bash
python -m harness.fault_injection.runner
polaris-fault-injection
```

Catalogue: `harness/fault_injection/scenarios.yaml`.
