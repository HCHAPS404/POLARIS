"""Load logical device YAML from configs/devices/."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]


def load_device_yaml(relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(f"device catalog not found: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"device YAML must be a mapping: {path}")
    return payload


def resolve_device_catalog(scenario: dict[str, Any]) -> dict[str, dict[str, Any]]:
    catalog = scenario.get("device_catalog")
    if not isinstance(catalog, dict):
        raise ValueError("scenario requires device_catalog mapping")
    return {name: load_device_yaml(str(path)) for name, path in catalog.items()}
