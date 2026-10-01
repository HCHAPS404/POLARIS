# simulation/python/rf

**Evidence:** IMPLEMENTED (SIMULATED analytic link budget)

Minimal RF helpers for Forge credibility and IoT comm models. Uses free-space path loss (FSPL) only — no terrain, multipath, or regulatory emission modelling.

| Symbol | Module | Notes |
|--------|--------|-------|
| FSPL | `link_budget.free_space_path_loss_db` | dB, distance m, frequency MHz |
| Rx power | `link_budget.received_power_dbm` | Tx + gain − FSPL − fixed loss |

IoT transport (`simulation/python/iot/comm.py`) consumes the same FSPL via `iot.sensors.link_rssi_dbm`.

**NOT IMPLEMENTED:** LoRa spreading factor, duty cycle, spectrum masks, or live RF measurements.
