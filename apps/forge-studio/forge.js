(async () => {
  const el = document.getElementById("demo-latest");
  if (!el) return;
  try {
    const res = await fetch("/v1/meta/demo-latest");
    if (!res.ok) throw new Error(String(res.status));
    const body = await res.json();
    if (body.latest_log) {
      el.textContent = `Último log demo: ${body.latest_log} (${body.utc})`;
    } else {
      el.textContent =
        "Aún no hay log en harness/demo/output — ejecuta make demo en el repositorio.";
    }
  } catch (err) {
    el.textContent = `No se pudo leer meta demo: ${err.message}`;
  }
})();
