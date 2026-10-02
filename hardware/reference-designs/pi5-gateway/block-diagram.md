# Pi 5 gateway — block diagram

**Evidence:** DESIGNED

```text
┌──────────────────────────────────────────────────────────┐
│ Raspberry Pi 5                                           │
│  ┌─────────────┐    USB/SPI    ┌──────────────────────┐  │
│  │ Linux       │◄─────────────►│ LoRa packet forwarder │  │
│  │ (ChirpStack │               │ (DESIGNED only)       │  │
│  │  DESIGNED)  │               └──────────┬───────────┘  │
│  └──────┬──────┘                          │ RF 868 MHz   │
│         │ MQTT/HTTP ingest (sim)          ▼              │
│         ▼                          ┌──────────────┐        │
│  ┌─────────────┐                   │ Gateway ANT  │        │
│  │ Buffer +    │                   └──────────────┘        │
│  │ time sync   │                                          │
│  └──────┬──────┘                                          │
│         │ Ethernet / LTE backhaul (scenario toggles down)  │
└─────────┼──────────────────────────────────────────────────┘
          ▼
   POLARIS API ingest (SIMULATED) / platform ingest routes
```

Backhaul failure is exercised via scenario YAML (`backhaul_down`) and `harness/fault-injection/run_faults.py`.
