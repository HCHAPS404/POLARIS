"""Parser tests: SIMULATED only, declared PHI mode, rainfall contract."""

from __future__ import annotations

import pytest

from domains.observations.parse import ObservationParseError, parse_observation

BASE = {
    "observation_id": "550e8400-e29b-41d4-a716-446655440099",
    "observed_at": "2026-10-01T11:00:00Z",
    "observed_property": "rainfall_mm",
    "value": 20.0,
    "unit": "mm",
    "quality_flag": "qc_pass",
    "source_id": "sim-gauge-x",
    "source": "polaris.synthetic",
    "data_class": "SIMULATED",
    "spatial_unit_id": "unit-x",
    "site_id": "co-bogota-demo",
    "country_iso": "CO",
    "phi_mode": "DETECTION",
    "geometry": {"type": "Point", "coordinates": [-74.07, 4.71]},
    "provenance": {"data_class": "SIMULATED"},
}


def test_parse_simulated_observation() -> None:
    obs = parse_observation(BASE)
    assert obs.data_class == "SIMULATED"
    assert obs.phi_mode == "DETECTION"
    assert obs.value == 20.0


def test_refuse_live_label() -> None:
    payload = {**BASE, "data_class": "LIVE"}
    with pytest.raises(ObservationParseError, match="LIVE"):
        parse_observation(payload)


def test_refuse_undeclared_mode() -> None:
    payload = {**BASE, "phi_mode": "AUTO"}
    with pytest.raises(ObservationParseError, match="phi_mode"):
        parse_observation(payload)


def test_refuse_negative_rainfall() -> None:
    payload = {**BASE, "value": -1}
    with pytest.raises(ObservationParseError, match="rainfall_mm"):
        parse_observation(payload)


def test_refuse_wrong_property() -> None:
    payload = {**BASE, "observed_property": "water_level_m"}
    with pytest.raises(ObservationParseError, match="rainfall_mm"):
        parse_observation(payload)


def test_parse_historical_replay_requires_event_time() -> None:
    payload = {
        **BASE,
        "data_class": "HISTORICAL_REPLAY",
        "observed_at": "2017-04-01T06:00:00Z",
        "quality_flag": "raw",
        "provenance": {
            "event_time": "2017-04-01T06:00:00Z",
            "accumulation": "3h",
            "citations": [{"url": "https://example.invalid/cite", "date": "2017-04-05"}],
        },
    }
    obs = parse_observation(payload)
    assert obs.data_class == "HISTORICAL_REPLAY"
    assert obs.observed_at == "2017-04-01T06:00:00Z"
    assert obs.provenance["event_time"] == obs.observed_at


def test_refuse_event_time_replaced_by_ingest() -> None:
    payload = {
        **BASE,
        "data_class": "HISTORICAL_REPLAY",
        "observed_at": "2026-10-01T16:00:00Z",
        "provenance": {
            "event_time": "2017-04-01T06:00:00Z",
            "ingested_at": "2026-10-01T16:00:00Z",
            "accumulation": "3h",
            "citations": [{"url": "https://example.invalid/cite"}],
        },
    }
    with pytest.raises(ObservationParseError, match="event_time"):
        parse_observation(payload)


def test_refuse_ingested_at_copied_to_event_time() -> None:
    payload = {
        **BASE,
        "data_class": "HISTORICAL_REPLAY",
        "observed_at": "2026-10-01T16:00:00Z",
        "provenance": {
            "event_time": "2026-10-01T16:00:00Z",
            "ingested_at": "2026-10-01T16:00:00Z",
            "accumulation": "3h",
            "citations": [{"url": "https://example.invalid/cite"}],
        },
    }
    with pytest.raises(ObservationParseError, match="ingested_at"):
        parse_observation(payload)
