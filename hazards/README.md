# Hazards

**Evidence:** IMPLEMENTED transparent PHI baselines for all in-tree hazard plugins

Per-phenomenon plugins. Individual-first. New packages still use `make scaffold-hazard NAME=...`, then replace placeholder with tested PHI.

| hazard_id | formula_version (baseline) |
|-----------|----------------------------|
| flood | flood.phi.rainfall-threshold.v0.1.0 |
| flash_flood | flash_flood.phi.rain-burst.v0.1.0 |
| landslide | landslide.phi.slope-moisture-rain.v0.1.0 |
| wildfire | wildfire.phi.fire-weather-pm.v0.1.0 |
| drought | drought.phi.precip-moisture.v0.1.0 |
| heat | heat.phi.heat-stress.v0.1.0 |
| cyclone | cyclone.phi.wind-pressure.v0.1.0 |
| smoke | smoke.phi.pm-visibility.v0.1.0 |
| earthquake | earthquake.phi.pga-shaking.v0.1.0 (RAPID_DETECTION/EEW only) |
| tsunami | tsunami.phi.event-wave.v0.1.0 (event-triggered) |
| volcano | volcano.phi.so2-ash.v0.1.0 |
| erosion_subsidence | erosion_subsidence.phi.cohesion-slope-rain.v0.1.0 |

Registry: `domains/hazards/registry.py`. API catalog: `GET /v1/hazards`.
