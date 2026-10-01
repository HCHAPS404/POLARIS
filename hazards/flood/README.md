# hazards/flood

**Evidence:** IMPLEMENTED rainfall-threshold PHI baseline (`flood.phi.rainfall-threshold.v0.1.0`)

See [ADR-0006](../../docs/adr/0006-flood-phi-rainfall-baseline.md).

- PHI from 1-hour rainfall accumulation; T0=10 mm, T1=80 mm
- `phi_mode` declared: DETECTION | NOWCAST | FORECAST (uncertainty band only)
- Exposure/vulnerability are **not** PHI inputs
- Hydrodynamics, IDF calibration, live gauges: NOT IMPLEMENTED
