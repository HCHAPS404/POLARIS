"""Site-configured exposure and vulnerability (v0.1). EXPERIMENTAL — not census data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from domains.common import EVIDENCE_EXPERIMENTAL
from domains.exposure.stub import ExposureStub, stub_exposure
from domains.vulnerability.stub import VulnerabilityStub, stub_vulnerability

ROOT = Path(__file__).resolve().parents[2]
SITES = ROOT / "configs" / "sites"

EV_CONFIG_VERSION = "site-ev.v0.1.0"
EXPOSURE_FORMULA = "exposure.site-config.v0.1.0"
VULNERABILITY_FORMULA = "vulnerability.site-config.v0.1.0"


@dataclass(frozen=True)
class SiteEvBundle:
    config_version: str
    site_id: str


def _load_site_yaml(site_id: str) -> dict[str, Any] | None:
    path = SITES / f"{site_id}.yaml"
    if not path.is_file():
        return None
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def resolve_exposure(*, site_id: str, spatial_unit_id: str) -> ExposureStub:
    site = _load_site_yaml(site_id)
    block = (site or {}).get("exposure_vulnerability") or {}
    units = block.get("units") or {}
    row = units.get(spatial_unit_id)
    if not isinstance(row, dict) or "exposure" not in row:
        return stub_exposure(spatial_unit_id)
    value = float(row["exposure"])
    return ExposureStub(
        spatial_unit_id=spatial_unit_id,
        value=value,
        formula_version=EXPOSURE_FORMULA,
        model_version=EV_CONFIG_VERSION,
        evidence=str(block.get("evidence") or EVIDENCE_EXPERIMENTAL),
        notes=(
            f"From configs/sites/{site_id}.yaml exposure_vulnerability.units "
            "(EXPERIMENTAL; not census or building stock)."
        ),
    )


def resolve_vulnerability(*, site_id: str, spatial_unit_id: str) -> VulnerabilityStub:
    site = _load_site_yaml(site_id)
    block = (site or {}).get("exposure_vulnerability") or {}
    units = block.get("units") or {}
    row = units.get(spatial_unit_id)
    if not isinstance(row, dict) or "vulnerability" not in row:
        return stub_vulnerability(spatial_unit_id)
    value = float(row["vulnerability"])
    return VulnerabilityStub(
        spatial_unit_id=spatial_unit_id,
        value=value,
        formula_version=VULNERABILITY_FORMULA,
        model_version=EV_CONFIG_VERSION,
        evidence=str(block.get("evidence") or EVIDENCE_EXPERIMENTAL),
        notes=(
            f"From configs/sites/{site_id}.yaml exposure_vulnerability.units "
            "(EXPERIMENTAL; not fragility curves)."
        ),
    )


def ev_config_version_for_site(site_id: str) -> str | None:
    site = _load_site_yaml(site_id)
    block = (site or {}).get("exposure_vulnerability") or {}
    if not block.get("units"):
        return None
    return str(block.get("version") or EV_CONFIG_VERSION)


def uses_site_config(site_id: str, spatial_unit_id: str) -> bool:
    site = _load_site_yaml(site_id)
    block = (site or {}).get("exposure_vulnerability") or {}
    units = block.get("units") or {}
    row = units.get(spatial_unit_id)
    return isinstance(row, dict) and "exposure" in row and "vulnerability" in row
