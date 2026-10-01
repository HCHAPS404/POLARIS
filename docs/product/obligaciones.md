# POLARIS — Obligaciones y estado

**Corte:** 2026-10-01 (post P1 merge + Stage E–G P2)  
**Release objetivo:** 2026-10-08  
**Fuente de verdad de código:** `main` @ **`bac103d`** (merge [PR #5](https://github.com/HCHAPS404/POLARIS/pull/5)) + draft P2 landslide/CAP/E/V

Leyenda: **Hecho** · **Parcial** · **Falta** · **Continuo**

---

## Git

| Obligación | Estado | Evidencia |
|------------|--------|-----------|
| Merge PR #5 PostGIS/LIVE/hydro | **Hecho** | SHA **`bac103d`** |
| P2 landslide + CAP draft + site E/V | **Parcial / PR abierto** | `feature/p2-landslide-baseline` |

---

## Cadena vertical

| Eslabón | Estado |
|---------|--------|
| Flood V1 SIMULATED | **Hecho** |
| IoT SIMULATED → gateway → V1 | **Hecho** |
| PostGIS dev + API `run_id` | **Hecho IMPLEMENTED** (limitaciones en adapters doc) |
| LIVE_INTEGRATED Open-Meteo | **Parcial IMPLEMENTED** |
| PHI lluvia + nivel (max merge) | **Hecho IMPLEMENTED** (ADR-0009) |
| Landslide PHI slope/moisture/rain | **Parcial IMPLEMENTED** (ADR-0010, PR P2; sin validación de campo) |
| CAP OFFICIAL | **Falta** — solo DRAFT/SIMULATION en PR P2 |
| Site E/V configurable | **Parcial EXPERIMENTAL** (PR P2) |
| CHI / PCB / Flutter APK | **Falta** |

---

## Siguiente ejecutable

1. Merge PR P2 cuando CI verde.  
2. OpenAPI bump para `format=cap` y fixture landslide.  
3. CI PostGIS service (opcional).  
4. Tercer hazard o compound documentado — fuera de este PR.  
5. No reclamar HISTORICALLY_VALIDATED / alertas OFFICIAL.

Copia en store: `/cursor/stores/bc-c1aa1eb2-6730-427d-9ae9-6d6926cea46f/docs/obligaciones.md`.
