# POLARIS — Obligaciones y estado

**Corte:** 2026-10-02 (complete hazard baselines + product polish)  
**Release objetivo:** `v1.0.0-response-quest` (RC)  
**Fuente de verdad de código:** `main` + PR polish local deploy

Leyenda: **Hecho** · **Parcial** · **Falta** · **Continuo**

---

## Git

| Obligación | Estado | Evidencia |
|------------|--------|-----------|
| Merge PR #5 PostGIS/LIVE/hydro | **Hecho** | SHA **`bac103d`** |
| Merge PR #6 landslide + CAP + site E/V | **Hecho** | SHA **`c629531`** |
| P2 CHI minimal + Vector shell | **Hecho** | Merge PR #7 → **`94a56eb`** |
| P3 Horizon Mobile + Forge + demo harness | **Hecho** | Merge PR #8 → main |
| P4 wildfire + fault injection + release prep | **Hecho** | Merge PR #9 → **`45b67c0`** |
| P5 RC prep (docs, RF, release workflow draft) | **Hecho** | PR #10 merged |
| Product polish + one-command local deploy | **Hecho** | merged main |
| 15 países INTEGRATION CASE + adaptadores nacionales | **Hecho IMPLEMENTED** | `feature/complete-country-adapters` |

---

## Cadena vertical

| Eslabón | Estado |
|---------|--------|
| Flood V1 SIMULATED | **Hecho** |
| IoT SIMULATED → gateway → V1 | **Hecho** |
| IoT fault injection (packet_loss / gateway_down) | **Hecho IMPLEMENTED** |
| RF FSPL link budget (SIMULATED) | **Hecho IMPLEMENTED** (P5) |
| PostGIS dev + API `run_id` | **Hecho IMPLEMENTED** |
| Docker compose demo (PostGIS + API + static apps) | **Hecho IMPLEMENTED** (polish PR) |
| LIVE_INTEGRATED Open-Meteo | **Hecho IMPLEMENTED** (15 sitios + catálogo nacional) |
| PHI lluvia + nivel (max merge) | **Hecho IMPLEMENTED** (ADR-0009) |
| Landslide PHI slope/moisture/rain | **Hecho IMPLEMENTED** (ADR-0010) |
| Wildfire PHI fire-weather-pm | **Hecho IMPLEMENTED** (ADR-0012) |
| Heat PHI | **Hecho IMPLEMENTED** (heat.phi.heat-stress.v0.1.0) |
| Flash flood / drought / cyclone / smoke / volcano / erosion PHI | **Hecho IMPLEMENTED** (baseline v0.1.0) |
| Earthquake PHI (RAPID_DETECTION/EEW, no predicción) | **Hecho IMPLEMENTED** |
| Tsunami PHI (solo event-triggered) | **Hecho IMPLEMENTED** |
| Catálogo API `GET /v1/hazards` + param `hazard_id` en assessments | **Hecho IMPLEMENTED** |
| CAP OFFICIAL | **Falta** — DRAFT/SIMULATION (`format=cap`) |
| Site E/V configurable | **Parcial EXPERIMENTAL** |
| CHI flood+landslide (minimal) | **Hecho IMPLEMENTED** (ADR-0011) |
| Vector console polish | **Hecho IMPLEMENTED** (polish PR) |
| Forge studio polish | **Hecho IMPLEMENTED** (polish PR) |
| Horizon MapLibre polish + optional tiles | **Hecho IMPLEMENTED** (polish PR) |
| Flutter APK minimal + WebView horizon | **Hecho IMPLEMENTED** (polish PR) |
| Demo script + reproducibility + technical overview | **Hecho** (P5) |
| Tag `v1.0.0-response-quest` | **Falta** — espera checklist + aprobación Helmut |
| PCB KiCad | **Falta** |

---

## Siguiente ejecutable

1. CI verde y merge PR adaptadores 15 países → `main`.  
2. Helmut valida `docker compose up` + Horizon/Vector en localhost.  
3. Publicar GitHub Release draft cuando apruebe tag.  
4. No reclamar HISTORICALLY_VALIDATED / alertas OFFICIAL / envío concurso sin aprobación.

Copia en store: `/cursor/stores/bc-c1aa1eb2-6730-427d-9ae9-6d6926cea46f/docs/obligaciones.md`.
