"""Compound assessment — paired hazard slices → CHI per spatial unit (v0.2)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from adapters.storage.simulated_json import load_fixture
from application.flood_assessment import run_flood_slice
from application.landslide_assessment import run_landslide_slice
from application.wildfire_assessment import run_wildfire_slice
from domains.common import DISCLAIMER
from domains.compound.chi_engine import CompoundChiInputs, build_chi_record, chi_summary
from domains.compound.chi_rules import ChiRule, load_rule
from domains.compound.site_pairs import CompoundSitePair, get_compound_site
from domains.provenance.index_record import IndexRecord


@dataclass(frozen=True)
class CompoundUnitChi:
    spatial_unit_id: str
    phi_by_hazard: dict[str, float]
    chi: IndexRecord

    @property
    def phi_flood(self) -> float:
        return self.phi_by_hazard.get("flood", 0.0)

    @property
    def phi_landslide(self) -> float:
        return self.phi_by_hazard.get("landslide", 0.0)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "spatial_unit_id": self.spatial_unit_id,
            "chi": self.chi.to_dict(),
        }
        for hazard_id, value in sorted(self.phi_by_hazard.items()):
            payload[f"phi_{hazard_id}"] = value
        if "flood" in self.phi_by_hazard and "landslide" in self.phi_by_hazard:
            payload["phi_flood"] = self.phi_flood
            payload["phi_landslide"] = self.phi_landslide
        return payload


@dataclass(frozen=True)
class CompoundChiResult:
    site_id: str
    run_id: str
    seed: int
    data_class: str
    disclaimer: str
    pair: CompoundSitePair
    rule: ChiRule
    units: tuple[CompoundUnitChi, ...]

    def to_dict(self) -> dict[str, Any]:
        records = tuple(u.chi for u in self.units)
        ha, hb = self.rule.hazard_ids
        fixture_by_hazard = dict(self.pair.hazard_fixtures)
        return {
            "site_id": self.site_id,
            "run_id": self.run_id,
            "seed": self.seed,
            "data_class": self.data_class,
            "disclaimer": self.disclaimer,
            "rule_id": self.rule.rule_id,
            "hazard_ids": list(self.rule.hazard_ids),
            "fixture_ids": fixture_by_hazard,
            "flood_fixture_id": fixture_by_hazard.get("flood"),
            "landslide_fixture_id": fixture_by_hazard.get("landslide"),
            "evidence": {
                "chi": "IMPLEMENTED (configurable rules v0.2)",
                "field_validation": "NOT CLAIMED",
                "official_alerting": "NOT_IMPLEMENTED",
            },
            "summary": chi_summary(records, rule=self.rule),
            "units": [unit.to_dict() for unit in self.units],
        }


def run_id_for(site_id: str, seed: int) -> str:
    return str(uuid5(NAMESPACE_URL, f"polaris:compound-chi:{site_id}:{seed}"))


def _run_hazard_slice(hazard_id: str, fixture: dict[str, Any], *, seed: int):
    if hazard_id == "flood":
        return run_flood_slice(fixture, seed=seed)
    if hazard_id == "landslide":
        return run_landslide_slice(fixture, seed=seed)
    if hazard_id == "wildfire":
        return run_wildfire_slice(fixture, seed=seed)
    raise ValueError(f"unsupported compound hazard {hazard_id!r}")


def run_compound_chi(*, site_id: str, seed: int = 42) -> CompoundChiResult:
    pair = get_compound_site(site_id)
    rule = load_rule(pair.rule_id)
    expected = rule.hazard_ids
    configured = tuple(h for h, _ in pair.hazard_fixtures)
    if configured != expected:
        raise ValueError(
            f"site {site_id!r} hazards {configured} do not match rule {rule.rule_id} {expected}"
        )

    slices = []
    for hazard_id, fixture_id in pair.hazard_fixtures:
        fixture = load_fixture(fixture_id)
        if fixture.get("site_id") != pair.fixture_site_id:
            raise ValueError(
                f"fixture {fixture_id!r} site_id must match "
                f"fixture_site_id={pair.fixture_site_id!r}"
            )
        slices.append(_run_hazard_slice(hazard_id, fixture, seed=seed))

    phi_maps = [{u.spatial_unit_id: u for u in sl.units} for sl in slices]
    shared_units = sorted(set(phi_maps[0]) & set(phi_maps[1]))
    if not shared_units:
        raise ValueError("no overlapping spatial_unit_id between compound fixtures")

    computed_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    run_id = run_id_for(site_id, seed)
    units: list[CompoundUnitChi] = []
    ha, hb = rule.hazard_ids

    for spatial_unit_id in shared_units:
        u_a = phi_maps[0][spatial_unit_id]
        u_b = phi_maps[1][spatial_unit_id]
        chi = build_chi_record(
            spatial_unit_id=spatial_unit_id,
            inputs=CompoundChiInputs(
                hazard_ids=(ha, hb),
                phi_values=(u_a.phi.value, u_b.phi.value),
                phi_formula_versions=(u_a.phi.formula_version, u_b.phi.formula_version),
                rule_id=rule.rule_id,
            ),
            source_ids=u_a.phi.source_ids + u_b.phi.source_ids,
            observed_at=u_a.phi.observed_at,
            computed_at=computed_at,
            quality_flags=tuple(
                sorted(set(u_a.phi.quality_flags + u_b.phi.quality_flags))
            ),
            data_class=u_a.observation.data_class,
            run_id=run_id,
            rule=rule,
        )
        units.append(
            CompoundUnitChi(
                spatial_unit_id=spatial_unit_id,
                phi_by_hazard={ha: u_a.phi.value, hb: u_b.phi.value},
                chi=chi,
            )
        )

    return CompoundChiResult(
        site_id=site_id,
        run_id=run_id,
        seed=seed,
        data_class=slices[0].data_class,
        disclaimer=DISCLAIMER,
        pair=pair,
        rule=rule,
        units=tuple(units),
    )
