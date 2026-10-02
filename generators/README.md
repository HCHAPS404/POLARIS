# Generators

**Evidence:** IMPLEMENTED (hazard, country, site, sensor, communication, scenario)

| Generator | Script | Taskfile | Make |
|-----------|--------|----------|------|
| hazard | `generators/hazard/scaffold.py` | `task scaffold:hazard NAME=…` | `make scaffold-hazard NAME=…` |
| country | `generators/country/scaffold.py` | `task scaffold:country ISO=…` | `make scaffold-country ISO=…` |
| site | `generators/site/scaffold.py` | `task scaffold:site ID=… COUNTRY=…` | `make scaffold-site ID=… COUNTRY=…` |
| sensor | `generators/sensor/scaffold.py` | `task scaffold:sensor NAME=…` | `make scaffold-sensor NAME=…` |
| communication | `generators/communication/scaffold.py` | `task scaffold:communication NAME=…` | `make scaffold-communication NAME=…` |
| scenario | `generators/scenario/scaffold.py` | `task scaffold:scenario NAME=…` | `make scaffold-scenario NAME=…` |

Each scaffold writes provenance JSON alongside generated YAML. Hazard scaffolds also create plugin code and tests.
