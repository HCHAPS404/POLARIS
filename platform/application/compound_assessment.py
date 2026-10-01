"""Compound assessment — paired flood + landslide slices → CHI per spatial unit."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from adapters.storage.simulated_json import load_fixture
from application.flood_assessment import run_flood_slice
from application.landslide_assessment import run_landslide_slice
from domains.common import DISCLAIMER
from domains.compound.chi_flood_landslide import (
    CompoundChiInputs,
    build_chi_record,
    chi_summary,
)
from domains.compound.site_pairs import CompoundSitePair, get_compound_site
from domains.provenance.index_record import IndexRecord


@dataclass(frozen=True)
class CompoundUnitChi:
    spatial_unit_id: str
    phi_flood: float
    phi_landslide: float
    chi: IndexRecord

    def to_dict(self) -> dict[str, Any]:
        return {
            "spatial_unit_id": self.spatial_unit_id,
            "phi_flood": self.phi_flood,
            "phi_landslide": self.phi_landslide,
            "chi": self.chi.to_dict(),
        }


@dataclass(frozen=True)
class CompoundChiResult:
    site_id: str
    run_id: str
    seed: int
    data_class: str
    disclaimer: str
    pair: CompoundSitePair
    units: tuple[CompoundUnitChi, ...]

    def to_dict(self) -> dict[str, Any]:
        records = tuple(u.chi for u in self.units)
        return {
            "site_id": self.site_id,
            "run_id": self.run_id,
            "seed": self.seed,
            "data_class": self.data_class,
            "disclaimer": self.disclaimer,
            "flood_fixture_id": self.pair.flood_fixture_id,
            "landslide_fixture_id": self.pair.landslide_fixture_id,
            "evidence": {
                "chi": "IMPLEMENTED (minimal rain coupling)",
                "field_validation": "NOT CLAIMED",
                "official_alerting": "NOT_IMPLEMENTED",
            },
            "summary": chi_summary(records),
            "units": [unit.to_dict() for unit in self.units],
        }


def run_id_for(site_id: str, seed: int) -> str:
    return str(uuid5(NAMESPACE_URL, f"polaris:compound-chi:{site_id}:{seed}"))


def run_compound_chi(*, site_id: str, seed: int = 42) -> CompoundChiResult:
    pair = get_compound_site(site_id)
    flood_fixture = load_fixture(pair.flood_fixture_id)
    landslide_fixture = load_fixture(pair.landslide_fixture_id)
    if flood_fixture.get("site_id") != site_id or landslide_fixture.get("site_id") != site_id:
        raise ValueError("compound fixtures must share the configured site_id")

    flood = run_flood_slice(flood_fixture, seed=seed)
    landslide = run_landslide_slice(landslide_fixture, seed=seed)

    flood_phi = {u.spatial_unit_id: u for u in flood.units}
    landslide_phi = {u.spatial_unit_id: u for u in landslide.units}
    shared_units = sorted(set(flood_phi) & set(landslide_phi))
    if not shared_units:
        raise ValueError("no overlapping spatial_unit_id between compound fixtures")

    computed_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    run_id = run_id_for(site_id, seed)
    units: list[CompoundUnitChi] = []

    for spatial_unit_id in shared_units:
        f_unit = flood_phi[spatial_unit_id]
        l_unit = landslide_phi[spatial_unit_id]
        chi = build_chi_record(
            spatial_unit_id=spatial_unit_id,
            inputs=CompoundChiInputs(
                phi_flood=f_unit.phi.value,
                phi_landslide=l_unit.phi.value,
                flood_formula_version=f_unit.phi.formula_version,
                landslide_formula_version=l_unit.phi.formula_version,
            ),
            source_ids=f_unit.phi.source_ids + l_unit.phi.source_ids,
            observed_at=f_unit.phi.observed_at,
            computed_at=computed_at,
            quality_flags=tuple(
                sorted(set(f_unit.phi.quality_flags + l_unit.phi.quality_flags))
            ),
            data_class=f_unit.observation.data_class,
            run_id=run_id,
        )
        units.append(
            CompoundUnitChi(
                spatial_unit_id=spatial_unit_id,
                phi_flood=f_unit.phi.value,
                phi_landslide=l_unit.phi.value,
                chi=chi,
            )
        )

    return CompoundChiResult(
        site_id=site_id,
        run_id=run_id,
        seed=seed,
        data_class=flood.data_class,
        disclaimer=DISCLAIMER,
        pair=pair,
        units=tuple(units),
    )
