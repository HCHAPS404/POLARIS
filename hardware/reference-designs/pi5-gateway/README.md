# Raspberry Pi 5 — edge gateway reference

**Evidence:** DESIGNED (logical gateway per ADR-0008)

Store-and-forward gateway for SIMULATED IoT vertical slices. Not a deployed network server.

## Block diagram

See [block-diagram.md](./block-diagram.md).

## BOM

See [bom.csv](./bom.csv) (**Evidence:** DESIGNED).

## Firmware / simulation alignment

- Python stub: `firmware/gateway/gateway_stub.py`
- Digital Testbed: `simulation/python/iot/gateway.py`
- Device profile: `configs/devices/gateway-pi5.yaml`

## KiCad

Gateway is primarily an SBC + USB LoRa concentrator hat — no custom POLARIS PCB required for the reference case. Any future hat spin would use a separate placeholder under `hardware/pcb/kicad/` with explicit NOT PRODUCTION banners.
