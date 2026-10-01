# Simulation

**Evidence:** V1 flood runner IMPLEMENTED · C++ add() IMPLEMENTED · full Digital Testbed DESIGNED

Digital Testbed (Python/C++20). Wokwi is not primary. See README_SIMULATION_ENGINEERING.md.

V1: `python -m simulation.python.run --scenario simulation/scenarios/flood-bogota-demo.yaml --seed 42`
reads a **SIMULATED** fixture and prints versioned PHI/GCI/risk JSON.

Historical replay: `python -m simulation.python.run --scenario simulation/scenarios/flood-mocoa-2017-replay.yaml --seed 42`
plus `python -m harness.backtesting.replay --seed 42` (EXPERIMENTAL evidence).
