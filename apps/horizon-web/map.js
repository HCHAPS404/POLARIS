/* Horizon: MapLibre layer over SIMULATED or HISTORICAL_REPLAY flood assessments. */
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
  const fixtureId = params.get("fixture_id") || "flood-bogota-demo";

  const status = document.getElementById("status");
  const map = new maplibregl.Map({
    container: "map",
    style: {
      version: 8,
      sources: {},
      layers: [
        {
          id: "background",
          type: "background",
          paint: { "background-color": "#d9e4ec" },
        },
      ],
    },
    center: [-74.07, 4.71],
    zoom: 11,
  });

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

  map.on("load", async () => {
    try {
      const response = await fetch(
        `${apiBase}/v1/map/geojson?fixture_id=${encodeURIComponent(fixtureId)}`
      );
      if (!response.ok) {
        throw new Error(`API ${response.status}`);
      }
      const geojson = await response.json();
      const allowed = new Set(["SIMULATED", "HISTORICAL_REPLAY"]);
      if (!allowed.has(geojson.data_class)) {
        throw new Error("refusing map layer that is not SIMULATED or HISTORICAL_REPLAY");
      }
      status.textContent =
        `Loaded ${geojson.features.length} ${geojson.data_class} units · ${fixtureId} · run ${geojson.run_id}`;

      geojson.features.forEach((feature) => {
        feature.properties.color = riskColor(feature.properties.operational_risk);
      });

      const first = geojson.features[0];
      if (first && first.geometry && first.geometry.type === "Polygon") {
        const ring = first.geometry.coordinates[0];
        const lon = ring.reduce((s, p) => s + p[0], 0) / ring.length;
        const lat = ring.reduce((s, p) => s + p[1], 0) / ring.length;
        map.setCenter([lon, lat]);
        if (geojson.data_class === "HISTORICAL_REPLAY") {
          map.setZoom(12);
        }
      }

      map.addSource("flood-slice", { type: "geojson", data: geojson });
      map.addLayer({
        id: "flood-fill",
        type: "fill",
        source: "flood-slice",
        paint: {
          "fill-color": ["get", "color"],
          "fill-opacity": 0.55,
        },
      });
      map.addLayer({
        id: "flood-line",
        type: "line",
        source: "flood-slice",
        paint: { "line-color": "#222", "line-width": 1.5 },
      });

      map.on("click", "flood-fill", (event) => {
        const props = event.features[0].properties;
        new maplibregl.Popup({ offset: 18, maxWidth: "280px", anchor: "left" })
          .setLngLat(event.lngLat)
          .setHTML(popupHtml(props))
          .addTo(map);
      });
    } catch (error) {
      status.textContent = `Cannot load assessments: ${error.message}. Start the API on :8000.`;
    }
  });
})();
