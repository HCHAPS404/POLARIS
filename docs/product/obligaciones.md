# POLARIS — Obligaciones y estado

**Corte:** 2026-10-01 (post merge P0+V1 + HISTORICAL_REPLAY)  
**Release objetivo:** 2026-10-08  
**Fuente de verdad de código:** `main` @ `01ce186` (P0+V1) más el PR `feature/v1-historical-replay` para replay.

Leyenda: **Hecho** · **Parcial** · **Falta** · **Continuo** (deber, no entrega única)

---

## 0. Cierre de git (antes de seguir construyendo)

| # | Obligación | Estado | Evidencia |
|---|------------|--------|-----------|
| 0.1 | Merge P0 a `main` | **Hecho** | [PR #1](https://github.com/HCHAPS404/POLARIS/pull/1) merge `689695c` |
| 0.2 | Merge V1 encima de P0 | **Hecho** | [PR #2](https://github.com/HCHAPS404/POLARIS/pull/2) merge GitHub `2bb7a22` (base stacked); V1 también en `main` vía `01ce186` |
| 0.3 | Tag `v0.1.0-foundation` | **Hecho** | Tag anotado en `01ce186` |

---

## 1. Orden de implementación (P0 → P6)

| Orden | Obligación | Estado | Qué hay | Qué falta |
|-------|------------|--------|---------|-----------|
| **P0** | Repositorio, arquitectura, CI, esquemas, país/sitio | **Hecho** | Contrato, árbol canónico, reglas, ADRs, CI, `/health`, 15 CountryProfile stub, compose PostGIS/NATS/MQTT | Migraciones DB reales |
| **P1** | Ingesta, GIS, base, API, fuente live, mapa público | **Parcial** | Esquemas observación; API `/v1/*`; mapa Horizon; fixture SIMULATED + HISTORICAL_REPLAY | Adapter live (nunca fake); PostGIS persistido; catálogo de fuentes real; GIS de producción |
| **P2** | Primer hazard, PHI, GCI, riesgo, alertas | **Parcial** | PHI inundación umbral lluvia; GCI v0.1.0; riesgo `PHI × E_stub × V_stub`; alerta DRAFT | E/V reales; calibración; CAP; política de alerta; hidrodinámica |
| **P3** | Simulación, sintético, replay, sensores, RF, energía | **Parcial** | Runner flood Bogotá seed 42; **HISTORICAL_REPLAY Mocoa 2017 (EXPERIMENTAL)** | Kernel C++/pybind11; sensor model; comunicaciones; energía; FAULT_INJECTION |
| **P4** | Más hazards, CHI, fault injection, casos país/sitio | **Falta** | Carpetas hazard scaffold | CHI; landslide/wildfire/heat/…; perfiles sitio no-demo |
| **P5** | APK, Vector, demo, backtesting | **Parcial** | Backtest Mocoa 2017 EXPERIMENTAL | Flutter APK; Vector profesional; Forge UI; backtest HISTORICALLY_VALIDATED |
| **P6** | PCB/CAD, más países, spec piloto físico | **Falta** | Árbol `hardware/` vacío documentado | KiCad, BOM, spec piloto Colombia |

---

## 2. Cadena vertical

| Eslabón | Estado | Notas |
|---------|--------|-------|
| DATA | Parcial | Fixture SIMULATED Bogotá + HISTORICAL_REPLAY Mocoa 2017 citado; no LIVE_INTEGRATED |
| OBSERVATION + proveniencia | Hecho | Rechaza `data_class=LIVE`; `event_time` no se sustituye por ingest |
| QUALITY / GCI | Hecho mínimo | `gci.v0.1.0` (SIMULATED 0.65, HISTORICAL_REPLAY 0.70) |
| HAZARD / PHI | Hecho baseline inundación | Umbrales 10/80 mm **demo**, no IDF |
| CHI | Falta | No implementar como número mágico |
| EXPOSURE / VULNERABILITY | Parcial | Stubs PLACEHOLDER |
| OPERATIONAL RISK | Hecho fórmula | No es probabilidad de inundación |
| ALERT DRAFT | Hecho | HITL; nunca OFFICIAL |
| API | Hecho | `/health`, observaciones, assessments, alerts, geojson, backtests |
| MAP Horizon | Hecho mínimo | `?fixture_id=`; no OSM; no PWA completa |
| Sensor sim → radio → gateway → misma cadena | Falta | Siguiente demo del contrato |
| Evento histórico → replay → métricas backtest | **Hecho (EXPERIMENTAL)** | Mocoa 2017; no HISTORICALLY_VALIDATED |

---

## 3. Calendario de entrega (1–8 oct)

| Día | Deber (workflow) | Estado |
|-----|------------------|--------|
| **1** Arquitectura / fundación | Repo, contratos, CI, perfiles, health, esqueleto sim | **Hecho en `main`** + tag `v0.1.0-foundation` |
| **2** Observación | Catálogo, adapters, PostGIS, mapa, shell móvil, sensor sim | **Parcial:** mapa + schema + replay; falta live, DB, móvil, sensores |
| **3** Inteligencia de hazard | Registry, flood/landslide/fire, replay | **Parcial:** flood baseline + replay Mocoa |
| **4** Riesgo + alertas | GCI, CHI, E, V, riesgo, CAP | **Parcial:** GCI + DRAFT; falta CHI, CAP, offline |
| **5** Evidencia de ingeniería | RF, energía, fault injection, Monte Carlo, backtests | **Parcial:** backtest EXPERIMENTAL; resto falta |
| **6** Producto | Horizon / Vector / Forge / APK / E2E | **Parcial:** Horizon mínimo |
| **7** Congelar evidencia | Manuales, paper, video, figuras | **Parcial:** figura backtest si se genera |
| **8** Freeze + RC | Clone limpio, tests, demo, tag `v1.0.0-response-quest` | **Falta** |

---

## 4. Deberes permanentes

| Deber | Estado |
|-------|--------|
| No predicción sísmica determinista / no 72 h universal | Continuo |
| Estados de evidencia honestos | Continuo — replay es EXPERIMENTAL, no fingir skill |
| Dominio sin FastAPI/Postgres/React | Continuo |
| Proveniencia en toda observación externa | Continuo — fixture + replay citados |
| Alertas oficiales solo con autoridad humana | Continuo — solo DRAFT |
| LLM fuera del path de PHI/CHI/alerta | Continuo |
| Sin secretos en git | Continuo |
| Conventional Commits, PRs cortos, `main` releasable | Continuo — P0/V1 en `main` |

---

## 5. Siguiente obligación ejecutable

1. Sensor simulado → canal → gateway → misma pipeline.  
2. Adapter **LIVE_INTEGRATED** real (o estado stale explícito) + PostGIS.  
3. Segundo hazard baseline (landslide o wildfire).  
4. No reclamar HISTORICALLY_VALIDATED hasta GT de extensión y acumulación 1 h honestos.
