# POLARIS — Obligaciones y estado

**Corte:** 2026-10-01 (post merge IoT + P1 slice)  
**Release objetivo:** 2026-10-08  
**Fuente de verdad de código:** `main` @ **`d68c076`** (merge [PR #4](https://github.com/HCHAPS404/POLARIS/pull/4) IoT sim) + P1 en PR PostGIS/live/hydro.

Leyenda: **Hecho** · **Parcial** · **Falta** · **Continuo**

---

## Git

| Obligación | Estado | Evidencia |
|------------|--------|-----------|
| Merge PR #3 replay Mocoa | **Hecho** | SHA `8f70a16` |
| Merge PR #4 IoT sim | **Hecho** | SHA **`d68c076`** |
| P1 PostGIS + LIVE + PHI hydro | **Parcial / en PR** | Ver PR #5 (draft) |

---

## Cadena vertical (actualizado)

| Eslabón | Estado |
|---------|--------|
| HISTORICAL_REPLAY Mocoa | **Parcial EXPERIMENTAL** |
| Sensor sim → gateway → misma pipeline V1 | **Hecho SIMULATED** (en `main`) |
| PostGIS persistencia local | **Parcial IMPLEMENTED** (PR P1; sin HA producción) |
| LIVE_INTEGRATED precipitación | **Parcial IMPLEMENTED** (Open-Meteo; stale si falla HTTP) |
| PHI lluvia + nivel hidro | **Parcial IMPLEMENTED** (`flood.phi.rainfall-hydro.v0.2.0` cuando hay `water_level_m`) |

---

## Siguiente ejecutable

1. Merge PR P1 cuando CI verde.  
2. Segundo hazard baseline (landslide o wildfire).  
3. Integración PostGIS en CI (servicio opcional) o ampliar tests de repositorio.  
4. No reclamar HISTORICALLY_VALIDATED / PCB producción / alertas OFFICIAL.

Copia en store: `/cursor/stores/.../docs/obligaciones.md`.
