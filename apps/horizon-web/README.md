# horizon-web

**Evidence:** IMPLEMENTED minimal MapLibre flood layer · full Horizon dashboard DESIGNED

Static page (no `package.json`, so CI web job still skips pnpm). Consumes
`GET /v1/map/geojson` from `platform/api`. Served at `/horizon/` when the API runs.

MapLibre uses a local background style (no OSM/API key). Polygons are the product
layer. Copy is decision-support only: SIMULATED data, DRAFT alerts, no “risk = 83%”.
