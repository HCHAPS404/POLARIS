# harness/fault-injection

**Evidence:** IMPLEMENTED (SIMULATED IoT fault scenarios)

Runs IoT scenarios with `gateway_down` and `packet_loss` fault flags.

```bash
python harness/fault-injection/run_faults.py
make harness-faults
```

Unit coverage: `tests/unit/test_iot_fault_injection.py`.
