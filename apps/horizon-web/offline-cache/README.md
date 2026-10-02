# Horizon offline cache layout

**Evidence:** DESIGNED (browser-side contract; minimal localStorage hook in parent app)

Horizon is a static MapLibre page. Offline behaviour is **decision-support only** — cached artefacts remain `SIMULATED` / `HISTORICAL_REPLAY` with disclaimers.

## Directory role (repo)

This folder documents the **on-disk / browser cache shape** operators may mirror on mobile or PWA builds. No service worker is shipped in V1.

## Manifest

See [manifest.schema.json](./manifest.schema.json) for the JSON envelope.

## Runtime hook

`../offline-cache.js` persists last-good GeoJSON + metadata under `localStorage` key `polaris.horizon.cache.v1` when the API fetch succeeds.

## Non-claims

- Not full offline GIS or tile pyramids
- Not an official warning cache
