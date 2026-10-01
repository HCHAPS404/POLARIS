# POLARIS — Obligaciones y estado

**Corte:** 2026-10-01 (post P3 merge PR #8)  
**Release objetivo:** 2026-10-08  
**Fuente de verdad de código:** `main` + draft PR #9 (P4)

Leyenda: **Hecho** · **Parcial** · **Falta** · **Continuo**

---

## Git

| Obligación | Estado | Evidencia |
|------------|--------|-----------|
| Merge PR #5 PostGIS/LIVE/hydro | **Hecho** | SHA **`bac103d`** |
| Merge PR #6 landslide + CAP + site E/V | **Hecho** | SHA **`c629531`** |
| P2 CHI minimal + Vector shell | **Hecho** | Merge PR #7 → **`94a56eb`** |
| P3 Horizon Mobile + Forge + demo harness | **Hecho** | Merge PR #8 → main |
| P4 wildfire + fault injection + release prep | **Parcial / PR abierto** | `feature/p4-wildfire-fault-release-prep` → PR #9 |

---

## Cadena vertical

| Eslabón | Estado |
|---------|--------|
| Flood V1 SIMULATED | **Hecho** |
| IoT SIMULATED → gateway → V1 | **Hecho** |
| IoT fault injection (packet_loss / gateway_down) | **Hecho IMPLEMENTED** (P4) |
| PostGIS dev + API `run_id` | **Hecho IMPLEMENTED** |
| LIVE_INTEGRATED Open-Meteo | **Parcial IMPLEMENTED** |
| PHI lluvia + nivel (max merge) | **Hecho IMPLEMENTED** (ADR-0009) |
| Landslide PHI slope/moisture/rain | **Hecho IMPLEMENTED** (ADR-0010) |
| Wildfire PHI fire-weather-pm | **Hecho IMPLEMENTED** (ADR-0012; P4 PR #9) |
| CAP OFFICIAL | **Falta** — DRAFT/SIMULATION (`format=cap`) |
| Site E/V configurable | **Parcial EXPERIMENTAL** |
| CHI flood+landslide (minimal) | **Hecho IMPLEMENTED** (ADR-0011) |
| Vector console minimal | **Hecho IMPLEMENTED** |
| Forge studio shell | **Hecho IMPLEMENTED** (PR #8) |
| Flutter APK minimal | **Hecho IMPLEMENTED** (PR #8; no app store) |
| Demo script + reproducibility checklist 2026-10-08 | **Hecho** (P4 manuals) |
| PCB KiCad | **Falta** |

---

## Siguiente ejecutable

1. Merge PR #9 cuando CI verde → marcar ready para freeze 2026-10-08.  
2. Coordinador / Helmut merge final.  
3. No reclamar HISTORICALLY_VALIDATED / alertas OFFICIAL.

Copia en store: `/cursor/stores/bc-c1aa1eb2-6730-427d-9ae9-6d6926cea46f/docs/obligaciones.md`.
