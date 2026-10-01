# POLARIS — Obligaciones y estado

**Corte:** 2026-10-01 (post P3 draft PR #8 mobile/forge)  
**Release objetivo:** 2026-10-08  
**Fuente de verdad de código:** `main` @ merge PR #7 + draft PR #8

Leyenda: **Hecho** · **Parcial** · **Falta** · **Continuo**

---

## Git

| Obligación | Estado | Evidencia |
|------------|--------|-----------|
| Merge PR #5 PostGIS/LIVE/hydro | **Hecho** | SHA **`bac103d`** |
| Merge PR #6 landslide + CAP + site E/V | **Hecho** | SHA **`c629531`** |
| P2 CHI minimal + Vector shell | **Hecho** | Merge PR #7 → **`94a56eb`** (main) |
| P3 Horizon Mobile + Forge + demo harness | **Parcial / PR abierto** | `feature/p3-horizon-mobile-forge` → PR #8 |

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
| CHI flood+landslide (minimal) | **Hecho IMPLEMENTED** (ADR-0011, PR #7) |
| Vector console minimal | **Hecho IMPLEMENTED** (PR #7) |
| Forge studio shell | **Parcial IMPLEMENTED** (PR #8 draft) |
| Flutter APK minimal | **Parcial IMPLEMENTED** (PR #8; no app store) |
| PCB KiCad | **Falta** |

---

## Siguiente ejecutable

1. Merge PR #8 cuando CI verde (freeze 2026-10-08).  
2. WebView Horizon en mobile (opcional post-freeze).  
3. OpenAPI bump si se exponen rutas nuevas de forge/mobile.  
4. No reclamar HISTORICALLY_VALIDATED / alertas OFFICIAL.

Copia en store: `/cursor/stores/bc-c1aa1eb2-6730-427d-9ae9-6d6926cea46f/docs/obligaciones.md`.
