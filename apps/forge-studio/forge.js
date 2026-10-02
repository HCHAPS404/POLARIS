(async () => {
  const demoEl = document.getElementById("demo-latest");
  if (demoEl) {
    try {
      const res = await fetch("/v1/meta/demo-latest");
      if (!res.ok) throw new Error(String(res.status));
      const body = await res.json();
      if (body.latest_log) {
        demoEl.textContent = `Último log demo: ${body.latest_log} (${body.utc})`;
      } else {
        demoEl.textContent =
          "Aún no hay log en harness/demo/output — ejecuta make demo en el repositorio.";
      }
    } catch (err) {
      demoEl.textContent = `No se pudo leer meta demo: ${err.message}`;
    }
  }

  const experimentsEl = document.getElementById("experiments");
  if (!experimentsEl) return;
  try {
    const res = await fetch("/v1/backtesting/experiments");
    if (!res.ok) throw new Error(String(res.status));
    const body = await res.json();
    const items = body.experiments || [];
    if (!items.length) {
      experimentsEl.textContent = "No hay experimentos registrados.";
      return;
    }
    experimentsEl.innerHTML = items
      .map((exp) => {
        const dl = exp.downloads || {};
        const links = Object.entries(dl)
          .map(
            ([key, href]) =>
              `<a href="${href}?seed=42" download>${key.replace(/_/g, " ")}</a>`
          )
          .join(" · ");
        return `<article class="card">
          <h2>${exp.title || exp.id}</h2>
          <p><code>${exp.evidence || "EXPERIMENTAL"}</code> · ${exp.id}</p>
          <p>${links}</p>
        </article>`;
      })
      .join("");
  } catch (err) {
    experimentsEl.textContent = `No se pudo cargar experimentos: ${err.message}`;
  }
})();
