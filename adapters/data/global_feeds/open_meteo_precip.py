"""Open-Meteo precipitation adapter — LIVE_INTEGRATED (one real HTTP source)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import NAMESPACE_URL, uuid5

import yaml

from domains.common import DATA_CLASS_LIVE_INTEGRATED, DISCLAIMER

ROOT = Path(__file__).resolve().parents[3]
CATALOG_PATH = ROOT / "configs" / "data" / "sources" / "open-meteo-precipitation.yaml"
OPEN_METEO_LICENSE = (
    "Open-Meteo API (https://open-meteo.com/en/license) — verify terms for your deployment."
)


@dataclass(frozen=True)
class LiveFetchResult:
    status: str  # ok | stale
    observation: dict[str, Any] | None
    error: str | None = None
    retrieved_at: str | None = None


def load_catalog() -> dict[str, Any]:
    return yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))


def load_site_profile(site_id: str) -> dict[str, Any]:
    path = ROOT / "configs" / "sites" / f"{site_id}.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"site profile not found: {site_id}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _http_get_json(url: str, *, timeout: float = 15.0) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "POLARIS/0.1 decision-support"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
    payload = json.loads(body)
    if not isinstance(payload, dict):
        raise ValueError("Open-Meteo response must be a JSON object")
    return payload


def build_forecast_url(*, lat: float, lon: float, endpoint: str) -> str:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "precipitation",
        "forecast_days": 1,
        "timezone": "UTC",
    }
    return f"{endpoint}?{urllib.parse.urlencode(params)}"


def precipitation_mm_from_response(payload: dict[str, Any]) -> tuple[float, str]:
    hourly = payload.get("hourly") or {}
    times = hourly.get("time") or []
    values = hourly.get("precipitation") or []
    if not times or not values:
        raise ValueError("Open-Meteo hourly precipitation missing")
    # Latest hour in the series as NOWCAST proxy (documented limitation).
    mm = float(values[-1])
    observed_at = str(times[-1])
    if not observed_at.endswith("Z"):
        observed_at = f"{observed_at}:00Z" if len(observed_at) == 16 else f"{observed_at}Z"
    return mm, observed_at


def fetch_open_meteo_precipitation(
    *,
    site_id: str = "co-bogota-demo",
    spatial_unit_id: str | None = None,
    phi_mode: str = "NOWCAST",
    http_get=_http_get_json,
) -> LiveFetchResult:
    retrieved_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    catalog = load_catalog()
    try:
        site = load_site_profile(site_id)
        coords = site.get("coordinates") or {}
        lat = float(coords["lat"])
        lon = float(coords["lon"])
        url = build_forecast_url(
            lat=lat,
            lon=lon,
            endpoint=str(catalog.get("endpoint")),
        )
        payload = http_get(url)
        mm, observed_at = precipitation_mm_from_response(payload)
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, FileNotFoundError) as exc:
        return LiveFetchResult(
            status="stale",
            observation=None,
            error=str(exc),
            retrieved_at=retrieved_at,
        )

    spatial = spatial_unit_id or f"{site_id}-catchment-north"
    obs_id = str(uuid5(NAMESPACE_URL, f"polaris:live:open-meteo:{site_id}:{observed_at}"))
    observation = {
        "observation_id": obs_id,
        "observed_at": observed_at,
        "observed_property": "rainfall_mm",
        "value": mm,
        "unit": "mm",
        "quality_flag": "raw",
        "source_id": str(catalog["source_id"]),
        "source": "open-meteo.com",
        "data_class": DATA_CLASS_LIVE_INTEGRATED,
        "spatial_unit_id": spatial,
        "site_id": site_id,
        "country_iso": str(site.get("country_iso", "CO")),
        "phi_mode": phi_mode,
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "provenance": {
            "adapter_id": "open_meteo_precip",
            "retrieved_at": retrieved_at,
            "license_note": OPEN_METEO_LICENSE,
            "source_url": url,
            "accumulation": "1h",
            "catalog_path": str(CATALOG_PATH.relative_to(ROOT)),
        },
    }
    return LiveFetchResult(status="ok", observation=observation, retrieved_at=retrieved_at)


def run_live_precip_slice(
    *,
    site_id: str = "co-bogota-demo",
    seed: int = 42,
    http_get=_http_get_json,
) -> dict[str, Any]:
    from application.flood_assessment import run_flood_slice, run_id_for

    fetch = fetch_open_meteo_precipitation(site_id=site_id, http_get=http_get)
    if fetch.status != "ok" or fetch.observation is None:
        return {
            "status": "stale",
            "data_class": DATA_CLASS_LIVE_INTEGRATED,
            "disclaimer": DISCLAIMER,
            "site_id": site_id,
            "retrieved_at": fetch.retrieved_at,
            "error": fetch.error,
            "observations": [],
            "flood_slice": None,
        }

    fixture_id = f"live-open-meteo-{site_id}"
    fixture = {
        "fixture_id": fixture_id,
        "data_class": DATA_CLASS_LIVE_INTEGRATED,
        "hazard_id": "flood",
        "site_id": site_id,
        "country_iso": fetch.observation["country_iso"],
        "as_of": fetch.retrieved_at,
        "disclaimer": DISCLAIMER,
        "observations": [fetch.observation],
    }
    slice_result = run_flood_slice(fixture, seed=seed)
    run_id = run_id_for(fixture_id, seed)
    return {
        "status": "ok",
        "data_class": DATA_CLASS_LIVE_INTEGRATED,
        "disclaimer": DISCLAIMER,
        "site_id": site_id,
        "run_id": run_id,
        "observations": [fetch.observation],
        "flood_slice": slice_result.to_dict(),
    }


def live_smoke_enabled() -> bool:
    return os.environ.get("POLARIS_LIVE_SMOKE", "").lower() in ("1", "true", "yes")
