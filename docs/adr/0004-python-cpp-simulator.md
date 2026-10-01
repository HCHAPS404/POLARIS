# ADR-0004 — Python + C++20 Digital Testbed (pybind11 / CMake)

**Evidence:** PLACEHOLDER IMPLEMENTED (C++ `add` + test). Bindings and runner DESIGNED.

## Status

Accepted — 2026-10-01

## Context

Hazard kernels need determinism, speed, and auditability. A notebook-only or Wokwi-only story cannot backtest floods or earthquakes.

## Decision

- **Python** orchestrates scenarios, I/O, reports (`simulation/python`)
- **C++20** holds numerical kernels (`simulation/cpp`), built with **CMake**
- **pybind11** will expose kernels (`simulation/bindings`) after P0
- **Wokwi is not primary** (see `README_SIMULATION_ENGINEERING.md`)

P0 ships a placeholder library and a failing-closed test (`1+2=3`), not physics.

## Alternatives

- Python only — acceptable for prototypes, weaker for heavy kernels
- Julia — extra toolchain for a three-person team
- Wokwi as the simulator — rejected

## Consequences

CI `cpp.yml` builds the placeholder when a compiler is present. Missing pybind11 wheels must not fail P0 Python jobs.

## Validation

`make test-cpp` or the C++ workflow compiles `polaris_placeholder` and runs `polaris_placeholder_test`.
