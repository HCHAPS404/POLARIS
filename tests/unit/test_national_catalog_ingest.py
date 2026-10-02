"""Contract tests for national catalog ingest (mocked HTTP)."""

from __future__ import annotations

import pytest

from adapters.data.national.catalog_ingest import (
    ingest_all_integration_countries,
    ingest_national_catalog,
    load_country_catalog,
    load_country_profile,
    result_to_dict,
)
from adapters.data.national.registry import list_integration_country_codes
from domains.common import DATA_CLASS_LIVE_INTEGRATED, DATA_CLASS_SIMULATED


def test_fifteen_iso_codes() -> None:
    codes = list_integration_country_codes()
    assert len(codes) == 15
    assert set(codes) == {
        "AU",
        "BD",
        "CA",
        "CL",
        "CN",
        "CO",
        "DE",
        "ES",
        "ET",
        "ID",
        "JP",
        "KE",
        "NZ",
        "PH",
        "US",
    }


@pytest.mark.parametrize("iso_code", list_integration_country_codes())
def test_country_profile_and_catalog_files(iso_code: str) -> None:
    profile = load_country_profile(iso_code)
    catalog = load_country_catalog(iso_code)
    assert profile["iso_code"] == iso_code
    assert profile["status"] == "INTEGRATION_CASE"
    integration = profile.get("integration") or {}
    assert integration.get("site_id")
    assert integration.get("region_id")
    assert catalog["country_iso"] == iso_code
    assert catalog.get("precipitation_binding", {}).get("site_id") == integration["site_id"]


def test_ingest_static_country_mocked() -> None:
    result = ingest_national_catalog("BD")
    assert result.status == "ok"
    assert result.data_class == DATA_CLASS_SIMULATED
    assert result.integration_site_id == "bd-dhaka-demo"
    payload = result_to_dict(result)
    assert payload["static_catalog"]["country_iso"] == "BD"


def test_ingest_us_live_mocked() -> None:
    def fake_http(url: str, headers: dict[str, str] | None) -> dict:
        assert "weather.gov" in url
        return {"features": [{"id": "a1"}, {"id": "a2"}]}

    result = ingest_national_catalog("US", http_get=fake_http)
    assert result.status == "ok"
    assert result.data_class == DATA_CLASS_LIVE_INTEGRATED
    assert result.live_metadata[0].status == "ok"
    assert result.live_metadata[0].payload["summary"]["alert_feature_count"] == 2


def test_ingest_us_stale_on_error() -> None:
    def boom(_url: str, _headers: dict[str, str] | None) -> dict:
        raise TimeoutError("down")

    result = ingest_national_catalog("US", http_get=boom)
    assert result.status == "stale"
    assert result.data_class == DATA_CLASS_LIVE_INTEGRATED
    assert result.error


def test_ingest_all_countries_smoke() -> None:
    results = ingest_all_integration_countries(
        http_get=lambda _u, _h: {"features": []},
    )
    assert len(results) == 15
