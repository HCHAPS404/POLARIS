const API = "";
const params = new URLSearchParams(window.location.search);

function qs(id) {
  return document.getElementById(id);
}

function table(headers, rows) {
  if (!rows.length) {
    return "<p>No rows.</p>";
  }
  const head = headers.map((h) => `<th>${h}</th>`).join("");
  const body = rows
    .map((cells) => `<tr>${cells.map((c) => `<td>${c}</td>`).join("")}</tr>`)
    .join("");
  return `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
}

async function fetchJson(path) {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) {
    throw new Error(`${path} → ${res.status}`);
  }
  return res.json();
}

function renderAssessments(label, body) {
  return (body.assessments || []).map((u) => [
    u.spatial_unit_id,
    label,
    body.data_class ?? "—",
    u.gci?.value?.toFixed(3) ?? "—",
    u.phi?.value?.toFixed(3) ?? "—",
    u.operational_risk?.value?.toFixed(3) ?? "—",
    u.alert?.level ?? "—",
    u.phi?.formula_version ?? "",
  ]);
}

function syncLinks(floodId) {
  qs("cap-link").href = `/v1/alerts?fixture_id=${encodeURIComponent(floodId)}&format=cap`;
  qs("horizon-link").href = `/horizon/?fixture_id=${encodeURIComponent(floodId)}`;
  const next = new URL(window.location.href);
  next.searchParams.set("fixture_id", floodId);
  window.history.replaceState({}, "", next);
}

function applyFixtureFromUrl() {
  const fromUrl = params.get("fixture_id");
  if (fromUrl) {
    const select = qs("flood-fixture");
    const hasOption = [...select.options].some((o) => o.value === fromUrl);
    if (hasOption) {
      select.value = fromUrl;
    }
  }
}

async function refresh() {
  const floodId = qs("flood-fixture").value;
  const landslideId = qs("landslide-fixture").value;
  const siteId = qs("compound-site").value;
  syncLinks(floodId);

  try {
    const [health, flood, landslide, chi, alerts] = await Promise.all([
      fetchJson("/health"),
      fetchJson(`/v1/assessments?fixture_id=${encodeURIComponent(floodId)}`),
      fetchJson(`/v1/assessments?fixture_id=${encodeURIComponent(landslideId)}`),
      fetchJson(`/v1/compound/chi?site_id=${encodeURIComponent(siteId)}`),
      fetchJson(`/v1/alerts?fixture_id=${encodeURIComponent(floodId)}`),
    ]);

    qs("status").textContent = `API ${health.status} · ${health.maturity} · ${health.utc}`;
    qs("storage-backend").textContent = health.storage_backend;

    const assessmentRows = [
      ...renderAssessments("flood", flood),
      ...renderAssessments("landslide", landslide),
    ];
    qs("assessments").innerHTML = table(
      ["Unit", "Hazard", "data_class", "GCI", "PHI", "Risk", "DRAFT level", "PHI formula"],
      assessmentRows,
    );

    const chiRows = (chi.units || []).map((u) => {
      const active = u.chi?.inputs?.interaction_active;
      const cls = active ? ' class="chi-active"' : "";
      return [
        u.spatial_unit_id,
        u.phi_flood?.toFixed(3),
        u.phi_landslide?.toFixed(3),
        `<span${cls}>${u.chi?.value?.toFixed(3)}</span>`,
        active ? "yes" : "no",
        u.chi?.formula_version ?? "",
      ];
    });
    qs("chi").innerHTML = table(
      ["Unit", "PHI flood", "PHI landslide", "CHI", "Active", "Formula"],
      chiRows,
    );

    const alertRows = (alerts.alerts || []).map((a) => [
      a.spatial_unit_id,
      a.level,
      a.status,
      a.hazard_id ?? "—",
      String(a.operational_risk_value ?? "—"),
    ]);
    qs("alerts").innerHTML = table(
      ["Unit", "Level", "Status", "Hazard", "Operational risk"],
      alertRows,
    );
  } catch (err) {
    qs("status").textContent = `Error: ${err.message}`;
  }
}

applyFixtureFromUrl();
["flood-fixture", "landslide-fixture", "compound-site"].forEach((id) => {
  qs(id).addEventListener("change", refresh);
});

refresh();
