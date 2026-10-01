"""Parse and reject dishonest observation payloads."""

from __future__ import annotations

from typing import Any

from domains.common import (
    ALLOWED_DATA_CLASSES,
    DATA_CLASS_HISTORICAL_REPLAY,
    DATA_CLASS_LIVE,
    DATA_CLASS_LIVE_INTEGRATED,
    PHI_MODES,
    QUALITY_FLAGS,
)
from domains.observations.models import Observation

REQUIRED_OBSERVATION_FIELDS = (
    "observation_id",
    "observed_at",
    "observed_property",
    "value",
    "unit",
    "quality_flag",
    "source_id",
    "source",
    "data_class",
    "spatial_unit_id",
    "site_id",
    "country_iso",
    "phi_mode",
)


class ObservationParseError(ValueError):
    """Fixture or payload cannot be used as an observation."""


def _require_historical_provenance(raw: dict[str, Any], provenance: dict[str, Any]) -> None:
    observed_at = str(raw["observed_at"])
    event_time = provenance.get("event_time")
    if not event_time:
        raise ObservationParseError(
            "HISTORICAL_REPLAY requires provenance.event_time (the documented event instant)"
        )
    if str(event_time) != observed_at:
        raise ObservationParseError(
            "event_time must equal observed_at; ingest time must not replace event time"
        )
    ingested_at = provenance.get("ingested_at")
    if ingested_at is not None and str(ingested_at) == observed_at:
        raise ObservationParseError(
            "ingested_at must not be copied onto observed_at / event_time"
        )
    citations = provenance.get("citations")
    if not isinstance(citations, list) or not citations:
        raise ObservationParseError("HISTORICAL_REPLAY requires non-empty provenance.citations")
    for citation in citations:
        if not isinstance(citation, dict) or not citation.get("url"):
            raise ObservationParseError("each citation must be an object with a url")
    accumulation = provenance.get("accumulation")
    if not accumulation:
        raise ObservationParseError("HISTORICAL_REPLAY requires provenance.accumulation")


def _require_live_integrated_provenance(provenance: dict[str, Any]) -> None:
    if not provenance.get("retrieved_at"):
        raise ObservationParseError("LIVE_INTEGRATED requires provenance.retrieved_at")
    if not provenance.get("license_note"):
        raise ObservationParseError("LIVE_INTEGRATED requires provenance.license_note")
    if not provenance.get("source_url"):
        raise ObservationParseError("LIVE_INTEGRATED requires provenance.source_url")
    adapter = provenance.get("adapter_id")
    if not adapter:
        raise ObservationParseError("LIVE_INTEGRATED requires provenance.adapter_id")


def parse_observation(raw: dict[str, Any]) -> Observation:
    if not isinstance(raw, dict):
        raise ObservationParseError("observation must be an object")

    data_class = raw.get("data_class")
    if data_class == DATA_CLASS_LIVE:
        raise ObservationParseError(
            "refusing data_class=LIVE (LIVE is not faked; adapters are NOT IMPLEMENTED)"
        )
    if data_class not in ALLOWED_DATA_CLASSES:
        raise ObservationParseError(
            "only data_class=SIMULATED, HISTORICAL_REPLAY, or LIVE_INTEGRATED are accepted; "
            f"refusing {data_class!r}"
        )
    missing = [name for name in REQUIRED_OBSERVATION_FIELDS if name not in raw]
    if missing:
        raise ObservationParseError(f"missing observation fields: {missing}")

    phi_mode = raw["phi_mode"]
    if phi_mode not in PHI_MODES:
        raise ObservationParseError(
            "phi_mode must be declared as DETECTION, NOWCAST, or FORECAST; "
            f"got {phi_mode!r}"
        )

    quality_flag = raw["quality_flag"]
    if quality_flag not in QUALITY_FLAGS:
        raise ObservationParseError(f"invalid quality_flag {quality_flag!r}")

    observed_property = str(raw["observed_property"])
    unit = str(raw["unit"])
    source_id = str(raw.get("source_id") or "")

    if observed_property == "rainfall_mm":
        if unit != "mm":
            raise ObservationParseError("rainfall observations require unit='mm'")
    elif observed_property == "water_level_m":
        if data_class == DATA_CLASS_LIVE_INTEGRATED:
            raise ObservationParseError(
                "LIVE_INTEGRATED water_level is not implemented; use SIMULATED IoT hydro"
            )
        if not source_id.startswith("iot/"):
            raise ObservationParseError(
                "water_level_m is accepted only for SIMULATED IoT sources (iot/*)"
            )
        if unit != "m":
            raise ObservationParseError("water_level observations require unit='m'")
    elif observed_property == "slope_deg":
        if unit != "deg":
            raise ObservationParseError("slope observations require unit='deg'")
    elif observed_property == "soil_moisture":
        if unit not in ("1", "dimensionless"):
            raise ObservationParseError("soil_moisture requires unit='1' or 'dimensionless'")
    else:
        raise ObservationParseError(
            "observed_property must be rainfall_mm, water_level_m (IoT), "
            "slope_deg, or soil_moisture"
        )

    try:
        value = float(raw["value"])
    except (TypeError, ValueError) as exc:
        raise ObservationParseError("observation value must be numeric") from exc
    if observed_property == "soil_moisture":
        if not 0 <= value <= 1:
            raise ObservationParseError("soil_moisture must be in [0, 1]")
    elif value < 0:
        raise ObservationParseError(f"{observed_property} must be >= 0")

    geometry = raw.get("geometry")
    if not isinstance(geometry, dict):
        raise ObservationParseError("geometry must be a GeoJSON object")

    provenance = raw.get("provenance") or {}
    if not isinstance(provenance, dict):
        raise ObservationParseError("provenance must be an object")
    if data_class == DATA_CLASS_HISTORICAL_REPLAY:
        _require_historical_provenance(raw, provenance)
    if data_class == DATA_CLASS_LIVE_INTEGRATED:
        _require_live_integrated_provenance(provenance)

    return Observation(
        observation_id=str(raw["observation_id"]),
        observed_at=str(raw["observed_at"]),
        observed_property=observed_property,
        value=value,
        unit=unit,
        quality_flag=str(quality_flag),
        source_id=str(raw["source_id"]),
        source=str(raw["source"]),
        data_class=str(data_class),
        spatial_unit_id=str(raw["spatial_unit_id"]),
        site_id=str(raw["site_id"]),
        country_iso=str(raw["country_iso"]),
        phi_mode=str(phi_mode),
        geometry=geometry,
        provenance=provenance,
    )


def parse_fixture(raw: dict[str, Any]) -> tuple[str, str, list[Observation]]:
    if not isinstance(raw, dict):
        raise ObservationParseError("fixture must be an object")
    data_class = raw.get("data_class")
    if data_class == DATA_CLASS_LIVE:
        raise ObservationParseError("fixture data_class=LIVE is refused (not faked)")
    if data_class not in ALLOWED_DATA_CLASSES:
        raise ObservationParseError(
            "fixture data_class must be SIMULATED, HISTORICAL_REPLAY, or LIVE_INTEGRATED"
        )
    fixture_id = str(raw.get("fixture_id") or "")
    if not fixture_id:
        raise ObservationParseError("fixture_id is required")
    as_of = str(raw.get("as_of") or "")
    if not as_of:
        raise ObservationParseError("fixture as_of timestamp is required")
    observations_raw = raw.get("observations")
    if not isinstance(observations_raw, list) or not observations_raw:
        raise ObservationParseError("fixture must contain a non-empty observations list")
    observations = [parse_observation(item) for item in observations_raw]
    for obs in observations:
        if obs.data_class != data_class:
            raise ObservationParseError("observation data_class must match fixture data_class")
    return fixture_id, as_of, observations
