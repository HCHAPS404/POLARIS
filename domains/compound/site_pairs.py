"""Registered compound sites — flood + landslide fixture pairs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "configs" / "compound"


@dataclass(frozen=True)
class CompoundSitePair:
    site_id: str
    flood_fixture_id: str
    landslide_fixture_id: str
    evidence: str
    notes: str


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def list_compound_sites() -> tuple[CompoundSitePair, ...]:
    if not CONFIG_DIR.is_dir():
        return ()
    pairs: list[CompoundSitePair] = []
    for path in sorted(CONFIG_DIR.glob("*.yaml")):
        raw = _load_yaml(path)
        pairs.append(
            CompoundSitePair(
                site_id=str(raw["site_id"]),
                flood_fixture_id=str(raw["flood_fixture_id"]),
                landslide_fixture_id=str(raw["landslide_fixture_id"]),
                evidence=str(raw.get("evidence", "IMPLEMENTED")),
                notes=str(raw.get("notes", "")),
            )
        )
    return tuple(pairs)


def get_compound_site(site_id: str) -> CompoundSitePair:
    for pair in list_compound_sites():
        if pair.site_id == site_id:
            return pair
    raise KeyError(f"no compound site registered for site_id={site_id!r}")
