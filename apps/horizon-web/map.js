/* Horizon V1: MapLibre layer over SIMULATED flood assessments. */
(() => {
  const apiBase = (() => {
    const param = new URLSearchParams(window.location.search).get("api");
    if (param) return param.replace(/\/$/, "");
    if (window.location.port === "8000" || window.location.pathname.startsWith("/horizon")) {
      return "";
    }
    return "http://127.0.0.1:8000";
  })();

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
      <div>rainfall: ${props.rainfall_mm} mm / 1h</div>
      <div>PHI: ${Number(props.phi).toFixed(4)} <small>${props.formula_version_phi}</small></div>
      <div>GCI: ${Number(props.gci).toFixed(4)} <small>${props.formula_version_gci}</small></div>
      <div>operational risk: ${Number(props.operational_risk).toFixed(4)} <small>${props.formula_version_risk}</small></div>
      <div>alert: ${props.alert_status} / ${props.alert_level}</div>
      <div>PHI uncertainty: ${props.uncertainty_phi}</div>
      <div>quality: ${props.quality_flag}</div>
      <p><em>Not a flood probability. DRAFT only.</em></p>
    `;
  }

  map.on("load", async () => {
    try {
      const response = await fetch(`${apiBase}/v1/map/geojson`);
      if (!response.ok) {
        throw new Error(`API ${response.status}`);
      }
      const geojson = await response.json();
      if (geojson.data_class !== "SIMULATED") {
        throw new Error("refusing map layer that is not SIMULATED");
      }
      status.textContent = `Loaded ${geojson.features.length} SIMULATED units · run ${geojson.run_id}`;

      geojson.features.forEach((feature) => {
        feature.properties.color = riskColor(feature.properties.operational_risk);
      });

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
