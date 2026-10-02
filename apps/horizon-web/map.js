/* Horizon: MapLibre over SIMULATED / HISTORICAL_REPLAY assessments. No LIVE. */
(() => {
  const params = new URLSearchParams(window.location.search);
  const apiBase = (() => {
    const param = params.get("api");
    if (param) return param.replace(/\/$/, "");
    if (window.location.port === "8000" || window.location.pathname.startsWith("/horizon")) {
      return "";
    }
    return "http://127.0.0.1:8000";
  })();

  let fixtureId = params.get("fixture_id") || "flood-bogota-demo";
  const LAYER_DEFS = {
    flood: { checkbox: "layer-flood", suffix: "", primary: true },
    landslide: {
      checkbox: "layer-landslide",
      fixture: "landslide-co-slope-demo",
      paint: { "fill-color": "#8c564b", "fill-opacity": 0.45 },
    },
    wildfire: {
      checkbox: "layer-wildfire",
      fixture: "wildfire-co-bogota-demo",
      paint: { "fill-color": "#d62728", "fill-opacity": 0.4 },
    },
    heat: {
      checkbox: "layer-heat",
      fixture: "heat-co-demo",
      paint: { "fill-color": "#ff7f0e", "fill-opacity": 0.42 },
    },
    flash_flood: {
      checkbox: "layer-flash_flood",
      fixture: "flash-flood-co-demo",
      paint: { "fill-color": "#1f78b4", "fill-opacity": 0.48 },
    },
    earthquake: {
      checkbox: "layer-earthquake",
      fixture: "earthquake-co-demo",
      paint: { "fill-color": "#9467bd", "fill-opacity": 0.45 },
    },
  };

  const statusEl = document.getElementById("status");
  const badgeEl = document.getElementById("data-class-badge");
  const freshnessEl = document.getElementById("freshness");
  const footerVersion = document.getElementById("footer-version");
  const footerStorage = document.getElementById("footer-storage");
  const errorBanner = document.getElementById("api-error-banner");
  const errorDetail = document.getElementById("api-error-detail");

  function showApiError(message) {
    if (!errorBanner) return;
    errorBanner.classList.remove("hidden");
    if (errorDetail) errorDetail.textContent = message ? ` ${message}` : "";
  }

  function clearApiError() {
    errorBanner?.classList.add("hidden");
    if (errorDetail) errorDetail.textContent = "";
  }

  async function refreshHealthFooter() {
    try {
      const res = await fetch(`${apiBase}/health`);
      if (!res.ok) throw new Error(`health ${res.status}`);
      const health = await res.json();
      if (footerVersion) {
        footerVersion.textContent = `${health.service} · ${health.maturity} · ${health.utc}`;
      }
      if (footerStorage) {
        footerStorage.textContent = `storage ${health.storage_backend}`;
      }
      clearApiError();
    } catch (err) {
      if (footerVersion) footerVersion.textContent = "API no alcanzable";
      if (footerStorage) footerStorage.textContent = "storage —";
      showApiError(err.message);
    }
  }
  const fixtureSelect = document.getElementById("fixture-select");
  const vectorLink = document.getElementById("vector-link");
  const tilesToggle = document.getElementById("tiles-toggle");

  if (fixtureSelect) {
    fixtureSelect.value = fixtureId;
    fixtureSelect.addEventListener("change", () => {
      fixtureId = fixtureSelect.value;
      syncUrl();
      reloadLayers();
    });
  }

  function syncUrl() {
    const next = new URL(window.location.href);
    next.searchParams.set("fixture_id", fixtureId);
    window.history.replaceState({}, "", next);
    if (vectorLink) {
      vectorLink.href = `/vector/?fixture_id=${encodeURIComponent(fixtureId)}`;
    }
  }
  syncUrl();

  let mapConfig = { tiles_enabled: false, tile_url_template: null };
  let map;

  function riskColor(value) {
    if (value >= 0.2) return "#e31a1c";
    if (value >= 0.1) return "#fd8d3c";
    if (value >= 0.05) return "#74c476";
    return "#c7e9c0";
  }

  function popupHtml(props) {
    return `
      <strong>${props.spatial_unit_id}</strong>
      <div>data_class: ${props.data_class}</div>
      <div>phi_mode (declared): ${props.phi_mode}</div>
      <div>event_time: ${props.observed_at || "n/a"}</div>
      <div>rainfall: ${props.rainfall_mm} mm / ${props.accumulation || "1h"}</div>
      <div>PHI: ${Number(props.phi).toFixed(4)} <small>${props.formula_version_phi}</small></div>
      <div>GCI: ${Number(props.gci).toFixed(4)} <small>${props.formula_version_gci}</small></div>
      <div>operational risk: ${Number(props.operational_risk).toFixed(4)} <small>${props.formula_version_risk}</small></div>
      <div>alert: ${props.alert_status} / ${props.alert_level}</div>
      <div>PHI uncertainty: ${props.uncertainty_phi}</div>
      <div>quality: ${props.quality_flag}</div>
      <p><em>Not a flood probability. DRAFT only. HISTORICAL_REPLAY is EXPERIMENTAL.</em></p>
    `;
  }

  function baseStyle() {
    const layers = [
      {
        id: "background",
        type: "background",
        paint: { "background-color": "#d9e4ec" },
      },
    ];
    const sources = {};
    if (tilesToggle?.checked && mapConfig.tile_url_template) {
      sources.osm = {
        type: "raster",
        tiles: [mapConfig.tile_url_template],
        tileSize: 256,
        attribution: mapConfig.attribution || "",
      };
      layers.push({
        id: "osm-raster",
        type: "raster",
        source: "osm",
        paint: { "raster-opacity": 0.85 },
      });
    }
    return { version: 8, sources, layers };
  }

  function ensureMap() {
    if (map) {
      return map;
    }
    map = new maplibregl.Map({
      container: "map",
      style: baseStyle(),
      center: [-74.07, 4.71],
      zoom: 11,
    });
    map.on("click", (e) => {
      const features = map.queryRenderedFeatures(e.point);
      const hit = features.find((f) => f.layer.id.startsWith("hazard-"));
      if (!hit) return;
      const props = hit.properties;
      new maplibregl.Popup({ offset: 18, maxWidth: "280px", anchor: "left" })
        .setLngLat(e.lngLat)
        .setHTML(popupHtml(props))
        .addTo(map);
    });
    return map;
  }

  function removeLayer(id) {
    if (map.getLayer(`${id}-fill`)) map.removeLayer(`${id}-fill`);
    if (map.getLayer(`${id}-line`)) map.removeLayer(`${id}-line`);
    if (map.getSource(id)) map.removeSource(id);
  }

  async function loadGeojson(layerId, fid) {
    const response = await fetch(
      `${apiBase}/v1/map/geojson?fixture_id=${encodeURIComponent(fid)}`,
    );
    if (!response.ok) {
      throw new Error(`${layerId} API ${response.status}`);
    }
    const geojson = await response.json();
    const allowed = new Set(["SIMULATED", "HISTORICAL_REPLAY"]);
    if (!allowed.has(geojson.data_class)) {
      throw new Error(`refusing ${geojson.data_class}`);
    }
    geojson.features.forEach((feature) => {
      feature.properties.color = riskColor(feature.properties.operational_risk);
    });
    if (layerId === "hazard-flood" && window.PolarisHorizonOffline) {
      window.PolarisHorizonOffline.saveManifest({
        schema_version: "horizon.offline.v0.1.0",
        data_class: geojson.data_class,
        fixture_id: fid,
        seed: 42,
        fetched_at: new Date().toISOString(),
        disclaimer: "Decision-support only. Not an official warning.",
        geojson,
      });
    }
    return geojson;
  }

  async function addLayer(layerId, fid, paintOverride) {
    removeLayer(layerId);
    const geojson = await loadGeojson(layerId, fid);
    map.addSource(layerId, { type: "geojson", data: geojson });
    const fillPaint = paintOverride || {
      "fill-color": ["get", "color"],
      "fill-opacity": 0.55,
    };
    map.addLayer({
      id: `${layerId}-fill`,
      type: "fill",
      source: layerId,
      paint: fillPaint,
    });
    map.addLayer({
      id: `${layerId}-line`,
      type: "line",
      source: layerId,
      paint: { "line-color": "#222", "line-width": 1.2 },
    });
    return geojson;
  }

  async function reloadLayers() {
    const m = ensureMap();
    statusEl.textContent = "Cargando capas…";
    try {
      let primaryMeta = null;
      if (document.getElementById(LAYER_DEFS.flood.checkbox)?.checked) {
        primaryMeta = await addLayer("hazard-flood", fixtureId);
      } else {
        removeLayer("hazard-flood");
      }

      for (const [key, def] of Object.entries(LAYER_DEFS)) {
        if (key === "flood") continue;
        const el = document.getElementById(def.checkbox);
        if (el?.checked) {
          await addLayer(`hazard-${key}`, def.fixture, def.paint);
        } else {
          removeLayer(`hazard-${key}`);
        }
      }

      if (primaryMeta) {
        badgeEl.textContent = primaryMeta.data_class;
        badgeEl.className = `badge dc-${primaryMeta.data_class.toLowerCase()}`;
        freshnessEl.textContent = `run ${primaryMeta.run_id} · ${primaryMeta.features.length} unidades · API ${apiBase || "(same origin)"}`;
        const first = primaryMeta.features[0];
        if (first?.geometry?.type === "Polygon") {
          const ring = first.geometry.coordinates[0];
          const lon = ring.reduce((s, p) => s + p[0], 0) / ring.length;
          const lat = ring.reduce((s, p) => s + p[1], 0) / ring.length;
          m.setCenter([lon, lat]);
          if (primaryMeta.data_class === "HISTORICAL_REPLAY") {
            m.setZoom(12);
          }
        }
        statusEl.textContent = `Principal: ${fixtureId}`;
      } else {
        badgeEl.textContent = "sin capa principal";
        statusEl.textContent = "Activa inundación u otra capa.";
      }
    } catch (error) {
      statusEl.textContent = `Error: ${error.message}. ¿API en :8000?`;
      badgeEl.textContent = "error";
      showApiError(error.message);
    }
  }

  function applyTileStyle() {
    if (!map) return;
    const center = map.getCenter();
    const zoom = map.getZoom();
    map.setStyle(baseStyle());
    map.once("styledata", () => {
      map.setCenter(center);
      map.setZoom(zoom);
      reloadLayers();
    });
  }

  tilesToggle?.addEventListener("change", applyTileStyle);
  Object.values(LAYER_DEFS).forEach((def) => {
    document.getElementById(def.checkbox)?.addEventListener("change", reloadLayers);
  });

  (async () => {
    await refreshHealthFooter();
    try {
      const cfgRes = await fetch(`${apiBase}/v1/config/map`);
      if (cfgRes.ok) {
        mapConfig = await cfgRes.json();
        if (tilesToggle) {
          tilesToggle.checked = Boolean(mapConfig.tiles_enabled);
          tilesToggle.disabled = !mapConfig.tile_url_template;
        }
      }
    } catch {
      /* local background only */
    }
    ensureMap();
    map.on("load", reloadLayers);
  })();
})();
