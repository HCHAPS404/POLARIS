# ADR-0008: Edge hardware reference (SIMULATED integration)

**Status:** Accepted  
**Date:** 2026-10-01  
**Evidence:** DESIGNED (reference boards; no production-ready PCB)

## Context

POLARIS needs a documented edge topology for simulated IoT vertical slices and future firmware work, without claiming deployed hardware.

## Decision

| Role | Reference hardware | Evidence in repo |
|------|-------------------|------------------|
| Field sensor node | **STM32 NUCLEO N657X0-Q** (STM32 N6 series) | `firmware/node/` stub; `configs/devices/*-node.yaml` |
| Edge gateway | **Raspberry Pi 5** | `firmware/gateway/` stub; `configs/devices/gateway-pi5.yaml`; `simulation/python/iot/gateway.py` |

Logical device types in V1 IoT slice: `weather-node`, `hydro-node`, `gateway-pi5` only.

KiCad/production PCB, antenna EM validation, and LoRaWAN network server deployment remain **P6 / FUTURE_WORK**.

## Consequences

- Simulation and firmware stubs align to these boards; swapping hardware requires a new ADR.
- No LIVE_INTEGRATED IoT adapters in this ADR.

## Validation

- `python -m simulation.python.iot_run --seed 42` produces deterministic SIMULATED observations with `source_id` prefix `iot/`.
- CI pytest covers sensor models, gateway store-and-forward, and flood pipeline.
