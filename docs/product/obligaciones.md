# POLARIS — Obligaciones y estado

**Corte:** 2026-10-01 (post P2 merge PR #6 + CHI/Vector PR #7 draft)  
**Release objetivo:** 2026-10-08  
**Fuente de verdad de código:** `main` @ **`c629531`** (merge [PR #6](https://github.com/HCHAPS404/POLARIS/pull/6)) + draft PR #7 CHI/Vector

Leyenda: **Hecho** · **Parcial** · **Falta** · **Continuo**

---

## Git

| Obligación | Estado | Evidencia |
|------------|--------|-----------|
| Merge PR #5 PostGIS/LIVE/hydro | **Hecho** | SHA **`bac103d`** |
| Merge PR #6 landslide + CAP + site E/V | **Hecho** | SHA **`c629531`** |
| P2 CHI minimal + Vector shell | **Parcial / PR abierto** | `feature/p2-chi-minimal-vector` → PR #7 |

---

## Cadena vertical

| Eslabón | Estado |
|---------|--------|
| Flood V1 SIMULATED | **Hecho** |
| IoT SIMULATED → gateway → V1 | **Hecho** |
| PostGIS dev + API `run_id` | **Hecho IMPLEMENTED** (limitaciones en adapters doc) |
| LIVE_INTEGRATED Open-Meteo | **Parcial IMPLEMENTED** |
| PHI lluvia + nivel (max merge) | **Hecho IMPLEMENTED** (ADR-0009) |
| Landslide PHI slope/moisture/rain | **Hecho IMPLEMENTED** (ADR-0010; sin validación de campo) |
| CAP OFFICIAL | **Falta** — DRAFT/SIMULATION (`format=cap`) |
| Site E/V configurable | **Parcial EXPERIMENTAL** |
| CHI flood+landslide (minimal) | **Parcial IMPLEMENTED** (ADR-0011, PR #7) |
| Vector console minimal | **Parcial IMPLEMENTED** (PR #7) |
| PCB / Flutter APK | **Falta** |

---

## Siguiente ejecutable

1. Merge PR #7 cuando CI verde.  
2. OpenAPI bump para compound CHI y Vector.  
3. Ampliar compound sites solo con ADR + fixtures emparejados.  
4. No reclamar HISTORICALLY_VALIDATED / alertas OFFICIAL.

Copia en store: `/cursor/stores/bc-c1aa1eb2-6730-427d-9ae9-6d6926cea46f/docs/obligaciones.md`.
