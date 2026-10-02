/** Persist last-good map payload for offline re-display (browser localStorage). */
(() => {
  const CACHE_KEY = "polaris.horizon.cache.v1";

  function saveManifest(manifest) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify(manifest));
    } catch (_err) {
      /* quota / private mode — ignore */
    }
  }

  function loadManifest() {
    try {
      const raw = localStorage.getItem(CACHE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (_err) {
      return null;
    }
  }

  window.PolarisHorizonOffline = { CACHE_KEY, saveManifest, loadManifest };
})();
