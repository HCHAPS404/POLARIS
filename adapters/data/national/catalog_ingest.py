"""National catalog ingest — metadata from YAML + optional keyless public HTTP sources."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

import yaml

from adapters.data.national.registry import (
    country_catalog_path,
    country_profile_path,
    list_integration_country_codes,
)
from domains.common import DATA_CLASS_LIVE_INTEGRATED, DATA_CLASS_SIMULATED, DISCLAIMER

HttpGetJson = Callable[[str, dict[str, str] | None], dict[str, Any]]

ROOT = Path(__file__).resolve().parents[3]
OPEN_METEO_CATALOG = ROOT / "configs" / "data" / "sources" / "open-meteo-precipitation.yaml"


@dataclass(frozen=True)
class LiveMetadataResult:
    source_id: str
    status: str  # ok | stale
    data_class: str
    payload: dict[str, Any] | None
    error: str | None = None
    endpoint: str | None = None


@dataclass(frozen=True)
class NationalCatalogIngestResult:
    country_iso: str
    status: str  # ok | partial | stale
    data_class: str
    catalog_id: str
    static_catalog: dict[str, Any]
    live_metadata: tuple[LiveMetadataResult, ...]
    integration_site_id: str | None
    retrieved_at: str
    disclaimer: str = DISCLAIMER
    error: str | None = None


def _http_get_json(
    url: str,
    headers: dict[str, str] | None = None,
    *,
    timeout: float = 15.0,
) -> dict[str, Any]:
    merged = {"User-Agent": "POLARIS/0.1 decision-support"}
    if headers:
        merged.update(headers)
    req = urllib.request.Request(url, headers=merged)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
    payload = json.loads(body)
    if not isinstance(payload, dict):
        raise ValueError("metadata response must be a JSON object")
    return payload


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be mapping: {path}")
    return data


def load_country_profile(iso_code: str) -> dict[str, Any]:
    return load_yaml(country_profile_path(iso_code))


def load_country_catalog(iso_code: str) -> dict[str, Any]:
    return load_yaml(country_catalog_path(iso_code))


def load_open_meteo_shared_catalog() -> dict[str, Any]:
    return load_yaml(OPEN_METEO_CATALOG)


def _summarize_metadata(source_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    if source_id.endswith("/nws-active-alerts"):
        features = payload.get("features") or []
        return {"alert_feature_count": len(features)}
    if source_id.endswith("/geonet-recent-quakes"):
        return {"quake_count": len(payload.get("features") or [])}
    if source_id.endswith("/jma-overview"):
        return {
            "report_datetime": payload.get("reportDatetime"),
            "text_blocks": len(payload.get("text") or []),
        }
    keys = list(payload.keys())[:12]
    return {"top_level_keys": keys, "key_count": len(payload)}


def fetch_live_metadata_source(
    source: dict[str, Any],
    *,
    http_get: HttpGetJson | None = None,
) -> LiveMetadataResult:
    getter = http_get or _http_get_json
    source_id = str(source["source_id"])
    endpoint = str(source["endpoint"])
    data_class = str(source.get("data_class", DATA_CLASS_LIVE_INTEGRATED))
    headers = source.get("headers")
    header_map = dict(headers) if isinstance(headers, dict) else None
    try:
        raw = getter(endpoint, header_map)
        summary = _summarize_metadata(source_id, raw)
        return LiveMetadataResult(
            source_id=source_id,
            status="ok",
            data_class=data_class,
            payload={
                "summary": summary,
                "sample_keys": list(raw.keys())[:8],
            },
            endpoint=endpoint,
        )
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        return LiveMetadataResult(
            source_id=source_id,
            status="stale",
            data_class=data_class,
            payload=None,
            error=str(exc),
            endpoint=endpoint,
        )


def ingest_national_catalog(
    iso_code: str,
    *,
    http_get: HttpGetJson | None = None,
) -> NationalCatalogIngestResult:
    iso = iso_code.upper()
    retrieved_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    profile = load_country_profile(iso)
    catalog_doc = load_country_catalog(iso)
    integration = profile.get("integration") or {}
    site_id = integration.get("site_id")
    catalog_id = str(catalog_doc.get("catalog_id", f"national/{iso.lower()}-v1"))

    static_catalog: dict[str, Any] = {
        "country_iso": iso,
        "country_name": profile.get("name"),
        "official_alert_authority": profile.get("official_alert_authority"),
        "priority_hazards": profile.get("priority_hazards") or [],
        "timezone": profile.get("timezone"),
        "integration_status": profile.get("status"),
        "catalog_id": catalog_id,
        "documented_sources": catalog_doc.get("documented_sources") or [],
        "precipitation_binding": catalog_doc.get("precipitation_binding"),
        "open_meteo_shared": load_open_meteo_shared_catalog(),
    }

    live_sources = catalog_doc.get("live_metadata_sources") or []
    live_results = tuple(
        fetch_live_metadata_source(src, http_get=http_get)
        for src in live_sources
        if isinstance(src, dict)
    )

    any_live = bool(live_sources)
    live_ok = sum(1 for r in live_results if r.status == "ok")
    live_stale = sum(1 for r in live_results if r.status == "stale")

    if not any_live:
        status = "ok"
        data_class = DATA_CLASS_SIMULATED
    elif live_ok and live_stale:
        status = "partial"
        data_class = DATA_CLASS_LIVE_INTEGRATED
    elif live_ok:
        status = "ok"
        data_class = DATA_CLASS_LIVE_INTEGRATED
    else:
        status = "stale"
        data_class = DATA_CLASS_LIVE_INTEGRATED

    error = None
    if status == "stale" and live_results:
        error = "; ".join(r.error or r.source_id for r in live_results if r.error)

    return NationalCatalogIngestResult(
        country_iso=iso,
        status=status,
        data_class=data_class,
        catalog_id=catalog_id,
        static_catalog=static_catalog,
        live_metadata=live_results,
        integration_site_id=str(site_id) if site_id else None,
        retrieved_at=retrieved_at,
        error=error,
    )


def ingest_all_integration_countries(
    *,
    http_get: HttpGetJson | None = None,
) -> list[NationalCatalogIngestResult]:
    codes = list_integration_country_codes()
    return [ingest_national_catalog(iso, http_get=http_get) for iso in codes]


def result_to_dict(result: NationalCatalogIngestResult) -> dict[str, Any]:
    return {
        "country_iso": result.country_iso,
        "status": result.status,
        "data_class": result.data_class,
        "catalog_id": result.catalog_id,
        "integration_site_id": result.integration_site_id,
        "retrieved_at": result.retrieved_at,
        "disclaimer": result.disclaimer,
        "error": result.error,
        "static_catalog": result.static_catalog,
        "live_metadata": [
            {
                "source_id": item.source_id,
                "status": item.status,
                "data_class": item.data_class,
                "endpoint": item.endpoint,
                "payload": item.payload,
                "error": item.error,
            }
            for item in result.live_metadata
        ],
    }
