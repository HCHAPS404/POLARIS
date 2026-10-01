"""Parse and reject dishonest observation payloads."""

from __future__ import annotations

from typing import Any

from domains.common import ALLOWED_DATA_CLASSES_V1, PHI_MODES, QUALITY_FLAGS
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
    """Fixture or payload cannot be used as a V1 observation."""


def parse_observation(raw: dict[str, Any]) -> Observation:
    if not isinstance(raw, dict):
        raise ObservationParseError("observation must be an object")

    data_class = raw.get("data_class")
    if data_class not in ALLOWED_DATA_CLASSES_V1:
        raise ObservationParseError(
            "V1 flood slice only accepts data_class=SIMULATED; "
            f"refusing {data_class!r} (LIVE/HISTORICAL are not faked)"
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

    if raw["observed_property"] != "rainfall_mm":
        raise ObservationParseError(
            "V1 flood baseline requires observed_property='rainfall_mm'"
        )
    if raw["unit"] != "mm":
        raise ObservationParseError("V1 flood baseline requires unit='mm'")

    try:
        value = float(raw["value"])
    except (TypeError, ValueError) as exc:
        raise ObservationParseError("rainfall value must be numeric") from exc
    if value < 0:
        raise ObservationParseError("rainfall_mm must be >= 0")

    geometry = raw.get("geometry")
    if not isinstance(geometry, dict):
        raise ObservationParseError("geometry must be a GeoJSON object")

    provenance = raw.get("provenance") or {}
    if not isinstance(provenance, dict):
        raise ObservationParseError("provenance must be an object")

    return Observation(
        observation_id=str(raw["observation_id"]),
        observed_at=str(raw["observed_at"]),
        observed_property="rainfall_mm",
        value=value,
        unit="mm",
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
    if raw.get("data_class") not in ALLOWED_DATA_CLASSES_V1:
        raise ObservationParseError(
            "fixture data_class must be SIMULATED; refusing live-labelled data"
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
    return fixture_id, as_of, observations
