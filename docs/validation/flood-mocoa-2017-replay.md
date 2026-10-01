# Mocoa 2017 HISTORICAL_REPLAY — EXPERIMENTAL backtest

**Evidence:** EXPERIMENTAL (not HISTORICALLY_VALIDATED)

**Scenario:** `flood-mocoa-2017-replay` · **seed:** 42 · **formulas:** same as V1
(`flood.phi.rainfall-threshold.v0.1.0`, `gci.v0.1.0`, `risk.operational.phi-ev-stub.v0.1.0`)

## Event

Overnight **31 March – 1 April 2017**, Mocoa (Putumayo, Colombia) experienced a
documented rainfall burst and urban debris flow / flash flood.

| Quantity | Value | Accumulation | Source |
|----------|-------|--------------|--------|
| 106 mm | 22:00–01:00 COT | 3 h | Decreto 599 de 2017 citing IDEAM |
| 129.3 mm | pluviometric day 31 Mar | 24 h | UNGRD repository (IDEAM Mocoa Acueducto); Decreto rounds to 129 mm |
| 1.3 mm | 01:00 COT 1 Apr | 1 h | Open-Meteo ERA5 (fetched) |

Citations (URLs, dates, license) are in `data/historical/flood-mocoa-2017.replay.json`.
Peak intensity 12.3 mm / 10 min (73.8 mm/h) from the UNGRD hydromet PDF is **not**
used as a 1-hour PHI input (that would confuse intensity with accumulation).

## Scoring rule (declared)

Positive prediction if **PHI ≥ 0.5**. Ground truth is **binary urban inundation
from official reports** (all three analysis windows share that GT). FAR is not
computed (no documented non-event unit). Brier is not published (PHI is not a
probability).

Expected under this fixture: **2 hits, 1 miss, POD = 2/3, FAR = omitted**.

The miss is the ERA5 1-hour value (1.3 mm < T0), which does not capture the
convective burst. The two hits apply 1-hour T0/T1 to 3-hour and 24-hour cited
totals — that **overstates** native 1-hour PHI and is a declared limitation.

## What this is not

- Not skill vs a mapped flood extent
- Not LIVE gauges
- Not HISTORICALLY_VALIDATED
- Not a debris-flow or hydrodynamic model
