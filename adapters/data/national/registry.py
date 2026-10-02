"""Integration country registry — fifteen ISO codes in scope (Helmut/Laura/Lenin list)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COUNTRIES_DIR = ROOT / "configs" / "countries"
CATALOG_DIR = ROOT / "configs" / "data" / "catalog"

INTEGRATION_COUNTRY_ISO_CODES: tuple[str, ...] = (
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
)


def list_integration_country_codes() -> list[str]:
    return list(INTEGRATION_COUNTRY_ISO_CODES)


def country_profile_path(iso_code: str) -> Path:
    return COUNTRIES_DIR / f"{iso_code.lower()}.yaml"


def country_catalog_path(iso_code: str) -> Path:
    return CATALOG_DIR / f"{iso_code.lower()}.yaml"
