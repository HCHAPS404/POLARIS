# N657X0-Q field node — block diagram

**Evidence:** DESIGNED (reference integration case, ADR-0008)

Not a production-ready schematic. KiCad sources live under `hardware/pcb/kicad/n657x0-q-node/` as a **placeholder path only** — not fab-ready.

## Logical blocks

```text
┌─────────────────────────────────────────────────────────────┐
│  STM32 NUCLEO N657X0-Q (NUCLEO-N657X0-Q)                  │
│  ┌──────────┐   I2C    ┌─────────────────┐                  │
│  │ STM32N6  │◄────────►│ Level driver    │  ultrasonic     │
│  │ + ST-LINK│          │ (hydro-node)    │                  │
│  └────┬─────┘   GPIO   └─────────────────┘                  │
│       │ pulse/count  ┌─────────────────┐                    │
│       └─────────────►│ Rain gauge      │  weather-node     │
│                      └─────────────────┘                    │
│       SPI/UART       ┌─────────────────┐                    │
│       └─────────────►│ LoRa sub-GHz    │──► ANT1 868 MHz   │
│                      │ (module stub)   │                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ LoRa (SIMULATED in Digital Testbed)
                              ▼
                    Raspberry Pi 5 gateway (reference)
```

## Firmware contract

- State machine: `firmware/node/main.c` (`BOOT → SAMPLE → TRANSMIT → SLEEP`)
- Payload shapes: `schemas/` + `simulation/python/iot/comm.py`
- Device YAML: `configs/devices/hydro-node.yaml`, `weather-node.yaml`

## Validation (software only)

- `python -m simulation.python.iot_run --scenario simulation/scenarios/iot-bogota-demo.yaml --seed 42`
- No in-repo RF chamber or conducted power measurements.
