# POLARIS — Obligaciones y estado

**Corte:** 2026-10-02 (post backlog #13–#16 en `main` @ `7a9281b`)  
**Release objetivo:** tag anotado **`v1.1.0-pre-local`** (bundle IEEE pre-integración local) · RC previo **`v1.0.0-response-quest`**

Leyenda: **Hecho** · **Parcial** · **Falta** · **Continuo**

---

## Git

| Obligación | Estado | Evidencia |
|------------|--------|-----------|
| Merge PR #5 PostGIS/LIVE/hydro | **Hecho** | SHA **`bac103d`** |
| Merge PR #6 landslide + CAP + site E/V | **Hecho** | SHA **`c629531`** |
| P2 CHI minimal + Vector shell | **Hecho** | Merge PR #7 → **`94a56eb`** |
| P3 Horizon Mobile + Forge + demo harness | **Hecho** | Merge PR #8 |
| P4 wildfire + fault injection + release prep | **Hecho** | Merge PR #9 → **`45b67c0`** |
| P5 RC prep (docs, RF, release workflow draft) | **Hecho** | PR #10 merged |
| Product polish + one-command local deploy | **Hecho** | PR #12 → **`0b233aa`** |
| 15 países INTEGRATION CASE + adaptadores nacionales | **Hecho IMPLEMENTED** | PR #13 → **`043c24f`** |
| P6 hardware refs + generadores + harness runners + UI stubs | **Hecho IMPLEMENTED** | PR #14 → **`523f518`** |
| CHI v0.2 + backtest Monte Carlo + RF/energía sim | **Hecho IMPLEMENTED** | PR #15 → **`93d0f70`** |
| Hazards backlog PHI baseline (plugins) | **Hecho IMPLEMENTED** | PR #16 → **`7a9281b`** |
| Ola 2 E2E cadena + docs + tag pre-local | **En curso** | PR `feature/ola2-pre-local-integration` |

---

## Cadena vertical

| Eslabón | Estado |
|---------|--------|
| Flood V1 SIMULATED | **Hecho** |
| IoT SIMULATED → gateway → V1 | **Hecho** |
| IoT fault injection (packet_loss / gateway_down) | **Hecho IMPLEMENTED** |
| RF FSPL link budget (SIMULATED) | **Hecho IMPLEMENTED** |
| PostGIS dev + API `run_id` | **Hecho IMPLEMENTED** |
| Docker compose demo (PostGIS + API + static apps) | **Hecho IMPLEMENTED** |
| LIVE_INTEGRATED Open-Meteo | **Hecho IMPLEMENTED** (15 sitios + catálogo nacional SIMULATED/INTEGRATION CASE) |
| PHI lluvia + nivel (max merge) | **Hecho IMPLEMENTED** |
| Landslide / wildfire / heat + backlog hazards PHI | **Hecho IMPLEMENTED** (baselines v0.1.0) |
| Catálogo API `GET /v1/hazards` | **Hecho IMPLEMENTED** |
| CAP OFFICIAL | **Falta** — DRAFT/SIMULATION (`format=cap`) |
| CHI flood+landslide + engine v0.2 | **Hecho IMPLEMENTED** |
| Forge / Vector / Horizon polish + offline stubs | **Parcial IMPLEMENTED** (#14 stubs) |
| E2E harness cadena (sim + pytest + optional PostGIS) | **Hecho IMPLEMENTED** (`make harness-e2e`) |
| Tag `v1.1.0-pre-local` | **Pendiente** — tras CI verde Ola 2 |
| Tag `v1.0.0-response-quest` publicado | **Hecho** (RC; no implica envío concurso) |
| PCB KiCad layout productivo | **Falta** |

---

## Siguiente ejecutable

1. Merge Ola 2 cuando CI verde → tag **`v1.1.0-pre-local`** en `main`.  
2. Helmut: `git pull` + `cp .env.example .env` + `docker compose up --build`; opcional `make harness-e2e --postgis` con DB local.  
3. Publicar GitHub Release draft del RC solo con aprobación humana.  
4. **No** reclamar HISTORICALLY_VALIDATED global, alertas OFFICIAL, ni concurso **submitted** sin envío humano.

Copia en store: `/cursor/stores/bc-c1aa1eb2-6730-427d-9ae9-6d6926cea46f/docs/obligaciones.md`.
