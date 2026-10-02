/**
 * Vector timelines stub — builds a minimal assessment timeline from API JSON.
 * Evidence: PLACEHOLDER UI (not a full incident timeline product).
 */
(() => {
  const container = document.getElementById("timelines");
  if (!container) return;

  /** @param {{ assessments?: Array<{ spatial_unit_id: string; as_of?: string }> }} payload */
  function renderTimeline(payload) {
    const rows = payload.assessments || [];
    if (!rows.length) {
      container.textContent = "Sin assessments para timeline.";
      return;
    }
    const items = rows
      .map((row) => {
        const when = row.as_of || row.observation?.event_time || "—";
        return `<li><code>${row.spatial_unit_id}</code> · ${when}</li>`;
      })
      .join("");
    container.innerHTML = `<ul class="timeline-list">${items}</ul>`;
  }

  window.PolarisVectorTimelines = { renderTimeline };
})();
