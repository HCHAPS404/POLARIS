# POLARIS — Ramas, PRs y etapas

**Corte:** 2026-10-02 (post #18 pulido web + mobile skeleton) · Repo: [HCHAPS404/POLARIS](https://github.com/HCHAPS404/POLARIS) · **`main`:** `c776f96`

## Tags en `main`

| Tag | Significado |
|-----|-------------|
| `v0.1.0-foundation` | Fin P0 (post V1 en main histórico) |
| `v1.0.0-response-quest` | Release candidate IEEE 2026 (SHA `2e0ff00` tras PR #11) |
| `v1.1.0-pre-local` | Bundle pre-integración local (post #13–#16; ver CHANGELOG) |

---

## Hecho — ramas mergeadas → `main`

| Etapa | PR | Rama | Merge SHA (abrev.) |
|-------|-----|------|---------------------|
| **P0 Fundación** | [#1](https://github.com/HCHAPS404/POLARIS/pull/1) | `feature/p0-foundation` | `689695c` |
| **V1 Flood vertical** | [#2](https://github.com/HCHAPS404/POLARIS/pull/2) | `feature/v1-flood-vertical-slice` | `01ce186` |
| **Replay histórico** | [#3](https://github.com/HCHAPS404/POLARIS/pull/3) | `feature/v1-historical-replay` | `8f70a16` |
| **IoT sim** | [#4](https://github.com/HCHAPS404/POLARIS/pull/4) | `feature/v1-iot-sim-pipeline` | `d68c076` |
| **P1 PostGIS + LIVE + PHI hidro** | [#5](https://github.com/HCHAPS404/POLARIS/pull/5) | `cursor/p1-postgis-observations-84c7` | `bac103d` |
| **P2 Landslide + CAP + E/V** | [#6](https://github.com/HCHAPS404/POLARIS/pull/6) | `feature/p2-landslide-baseline` | `c629531` |
| **P2 CHI + Vector** | [#7](https://github.com/HCHAPS404/POLARIS/pull/7) | `feature/p2-chi-minimal-vector` | `94a56eb` |
| **P3 Mobile + Forge + demo** | [#8](https://github.com/HCHAPS404/POLARIS/pull/8) | `feature/p3-horizon-mobile-forge` | `db90e8a` |
| **P4 Wildfire + fault + docs RC** | [#9](https://github.com/HCHAPS404/POLARIS/pull/9) | `feature/p4-wildfire-fault-release-prep` | `45b67c0` |
| **P5 RC prep (FSPL, overview)** | [#10](https://github.com/HCHAPS404/POLARIS/pull/10) | `feature/p5-release-candidate-prep` | `ba146ab` |
| **Release tag / CHANGELOG** | [#11](https://github.com/HCHAPS404/POLARIS/pull/11) | `cursor/release-tag-v1-3da7` | `2e0ff00` |
| **Pulido + Docker local** | [#12](https://github.com/HCHAPS404/POLARIS/pull/12) | `feature/polish-product-local-deploy` | `0b233aa` |
| **Ola 2 pre-local integration** | [#17](https://github.com/HCHAPS404/POLARIS/pull/17) | `feature/ola2-pre-local-integration` | `b528e8f` |
| **Pulido web + Horizon Mobile skeleton** | [#18](https://github.com/HCHAPS404/POLARIS/pull/18) | `feature/polish-web-mobile-structure` | `c776f96` |

---

## Backlog oct 2026 — mergeado a `main`

| Etapa | PR | Rama | Merge SHA |
|-------|-----|------|-----------|
| **15 países + catálogo nacional** | [#13](https://github.com/HCHAPS404/POLARIS/pull/13) | `cursor/complete-country-adapters-82e4` | `043c24f` |
| **P6 hardware + generadores + harness + UI stubs** | [#14](https://github.com/HCHAPS404/POLARIS/pull/14) | `feature/complete-hardware-ui-harnesses` | `523f518` |
| **Forge CHI v0.2 + backtest Monte Carlo + RF/energía** | [#15](https://github.com/HCHAPS404/POLARIS/pull/15) | `feature/complete-forge-chi-backtest` | `93d0f70` |
| **Hazards backlog (PHI baseline plugins)** | [#16](https://github.com/HCHAPS404/POLARIS/pull/16) | `feature/complete-hazards` | `7a9281b` |

Notas merge: #14 primero; #15 rebased sobre `main` (conflictos en `pyproject.toml`, `harness/fault-injection/README.md`); #16 rebased sin conflictos. CI verde antes de merge; #15 y #16 salieron de draft.

---

## Ola 2 — mergeada

| Etapa | PR | Rama | Notas |
|-------|-----|------|-------|
| **Pre-local integration** | [#17](https://github.com/HCHAPS404/POLARIS/pull/17) | `feature/ola2-pre-local-integration` | Tag `v1.1.0-pre-local` @ `b528e8f` (anterior a #18; usar `main` HEAD para prueba local) |

Copia sincronizada en store: `/cursor/stores/bc-c1aa1eb2-6730-427d-9ae9-6d6926cea46f/docs/ramas-y-etapas.md`.

---

## Falta — etapas futuras (plan)

| Etapa | Contenido típico |
|-------|------------------|
| **Local polish** | Validación Helmut `docker compose up` + Horizon/Vector + [guía mobile](../manuals/horizon-mobile-test-guide.md) |
| **Sim → web/mobile** | Runners registran vía API (ver `docs/product/mobile-data-flow.md`) — fase posterior |
| **Calibración hazards** | Baselines #16 → calibración; sin HISTORICALLY_VALIDATED global |
| **P6 Hardware productivo** | KiCad layout, firmware N657X0-Q |
| **IEEE evidencia** | Release publicada, video, paper (envío humano) |

No reclamar envío al concurso ni alertas OFFICIAL sin aprobación explícita.
