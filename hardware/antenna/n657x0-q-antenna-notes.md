# Antenna notes — N657X0-Q field node

**Evidence:** DESIGNED (link budget stub only)

## Intent

Document the **868 MHz sub-GHz** reference used in SIMULATED IoT scenarios (`communication.frequency_mhz: 868.0`). No measured radiation patterns, no certification (FCC / ANATEL / CE).

## Simulation cross-check

Use `simulation/python/rf/link_budget.py` (FSPL stub) with scenario distance and TX/RX parameters — **SIMULATED**, not calibrated to this BOM.

## Mechanical / placement (design guidance)

- Keep feedline short; avoid routing digital switching noise adjacent to RF section on any future custom PCB.
- Ground plane continuity under monopole or PCB antenna keep-out is assumed in link budget placeholders only.
- Field installs require site-specific clearance and local regulations — **not validated in this repository**.

## Explicit non-claims

- No TRP/TIS, no anechoic chamber data
- No LoRaWAN network server interoperability certificate
