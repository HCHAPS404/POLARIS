# POLARIS — Obligaciones y estado

**Corte:** 2026-10-02 (P5 RC prep, PR #10)  
**Release objetivo:** 2026-10-08  
**Fuente de verdad de código:** `main` + draft PR #10 (P5)

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
| P5 RC prep (docs, RF, release workflow draft) | **Parcial / PR abierto** | `feature/p5-release-candidate-prep` → PR #10 |

---

## Cadena vertical

| Eslabón | Estado |
|---------|--------|
| Flood V1 SIMULATED | **Hecho** |
| IoT SIMULATED → gateway → V1 | **Hecho** |
| IoT fault injection (packet_loss / gateway_down) | **Hecho IMPLEMENTED** |
| RF FSPL link budget (SIMULATED) | **Hecho IMPLEMENTED** (P5) |
| PostGIS dev + API `run_id` | **Hecho IMPLEMENTED** |
| LIVE_INTEGRATED Open-Meteo | **Parcial IMPLEMENTED** |
| PHI lluvia + nivel (max merge) | **Hecho IMPLEMENTED** (ADR-0009) |
| Landslide PHI slope/moisture/rain | **Hecho IMPLEMENTED** (ADR-0010) |
| Wildfire PHI fire-weather-pm | **Hecho IMPLEMENTED** (ADR-0012) |
| Heat PHI | **Falta** — registry PLACEHOLDER (P5) |
| CAP OFFICIAL | **Falta** — DRAFT/SIMULATION (`format=cap`) |
| Site E/V configurable | **Parcial EXPERIMENTAL** |
| CHI flood+landslide (minimal) | **Hecho IMPLEMENTED** (ADR-0011) |
| Vector console minimal | **Hecho IMPLEMENTED** |
| Forge studio shell | **Hecho IMPLEMENTED** |
| Flutter APK minimal | **Hecho IMPLEMENTED** (CI debug APK) |
| Demo script + reproducibility + technical overview | **Hecho** (P5) |
| Tag `v1.0.0-response-quest` | **Falta** — espera checklist + aprobación Helmut |
| PCB KiCad | **Falta** |

---

## Siguiente ejecutable

1. CI verde en PR #10 (python, postgis, mobile/flutter apk, web, security).  
2. Merge PR #10 → freeze 2026-10-08.  
3. Helmut aprueba tag; entonces `git tag v1.0.0-response-quest` (workflow draft release).  
4. No reclamar HISTORICALLY_VALIDATED / alertas OFFICIAL / envío concurso sin aprobación.

Copia en store: `/cursor/stores/bc-c1aa1eb2-6730-427d-9ae9-6d6926cea46f/docs/obligaciones.md`.
