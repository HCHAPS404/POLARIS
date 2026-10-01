"""Contract tests for Open-Meteo LIVE_INTEGRATED adapter (mocked HTTP)."""

from __future__ import annotations

import json

import pytest

from adapters.data.global_feeds.open_meteo_precip import (
    fetch_open_meteo_precipitation,
    precipitation_mm_from_response,
    run_live_precip_slice,
)
from domains.common import DATA_CLASS_LIVE_INTEGRATED
from domains.observations.parse import parse_observation

SAMPLE_RESPONSE = {
    "hourly": {
        "time": ["2026-10-01T11:00", "2026-10-01T12:00"],
        "precipitation": [0.5, 3.2],
    }
}


def test_precipitation_parser() -> None:
    mm, observed_at = precipitation_mm_from_response(SAMPLE_RESPONSE)
    assert mm == pytest.approx(3.2)
    assert observed_at.endswith("Z")


def test_fetch_ok_mocked() -> None:
    def fake_http(_url: str) -> dict:
        return SAMPLE_RESPONSE

    result = fetch_open_meteo_precipitation(site_id="co-bogota-demo", http_get=fake_http)
    assert result.status == "ok"
    assert result.observation is not None
    assert result.observation["data_class"] == DATA_CLASS_LIVE_INTEGRATED
    parse_observation(result.observation)


def test_fetch_stale_on_http_error() -> None:
    def boom(_url: str) -> dict:
        raise TimeoutError("network down")

    result = fetch_open_meteo_precipitation(site_id="co-bogota-demo", http_get=boom)
    assert result.status == "stale"
    assert result.observation is None
    assert result.error


def test_run_live_slice_mocked() -> None:
    def fake_http(_url: str) -> dict:
        return SAMPLE_RESPONSE

    payload = run_live_precip_slice(site_id="co-bogota-demo", seed=42, http_get=fake_http)
    assert payload["status"] == "ok"
    assert payload["flood_slice"]["data_class"] == DATA_CLASS_LIVE_INTEGRATED
    assert json.dumps(payload["observations"][0])
