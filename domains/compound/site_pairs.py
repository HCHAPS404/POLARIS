"""Registered compound sites — hazard fixture pairs + rule_id (CHI v0.2)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "configs" / "compound"


@dataclass(frozen=True)
class CompoundSitePair:
    site_id: str
    rule_id: str
    hazard_fixtures: tuple[tuple[str, str], ...]
    fixture_site_id: str
    evidence: str
    notes: str

    @property
    def flood_fixture_id(self) -> str:
        for hazard_id, fixture_id in self.hazard_fixtures:
            if hazard_id == "flood":
                return fixture_id
        raise AttributeError("site has no flood fixture")

    @property
    def landslide_fixture_id(self) -> str:
        for hazard_id, fixture_id in self.hazard_fixtures:
            if hazard_id == "landslide":
                return fixture_id
        raise AttributeError("site has no landslide fixture")


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _parse_site(raw: dict) -> CompoundSitePair:
    site_id = str(raw["site_id"])
    rule_id = str(raw.get("rule_id") or "flood-landslide-rain-coupling")
    if "hazards" in raw:
        hazards = raw["hazards"]
        if not isinstance(hazards, list) or len(hazards) != 2:
            raise ValueError(f"compound site {site_id} must list exactly two hazards")
        hazard_fixtures = tuple(
            (str(row["hazard_id"]), str(row["fixture_id"])) for row in hazards
        )
    else:
        hazard_fixtures = (
            ("flood", str(raw["flood_fixture_id"])),
            ("landslide", str(raw["landslide_fixture_id"])),
        )
    fixture_site_id = str(raw.get("fixture_site_id") or site_id)
    return CompoundSitePair(
        site_id=site_id,
        rule_id=rule_id,
        hazard_fixtures=hazard_fixtures,
        fixture_site_id=fixture_site_id,
        evidence=str(raw.get("evidence", "IMPLEMENTED")),
        notes=str(raw.get("notes", "")),
    )


def list_compound_sites() -> tuple[CompoundSitePair, ...]:
    if not CONFIG_DIR.is_dir():
        return ()
    pairs: list[CompoundSitePair] = []
    for path in sorted(CONFIG_DIR.glob("*.yaml")):
        if path.parent.name == "rules":
            continue
        raw = _load_yaml(path)
        if isinstance(raw, dict):
            pairs.append(_parse_site(raw))
    return tuple(pairs)


def get_compound_site(site_id: str) -> CompoundSitePair:
    for pair in list_compound_sites():
        if pair.site_id == site_id:
            return pair
    raise KeyError(f"no compound site registered for site_id={site_id!r}")
