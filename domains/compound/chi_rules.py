"""Load configurable compound CHI rules from configs/compound/rules/."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
RULES_DIR = ROOT / "configs" / "compound" / "rules"

SUPPORTED_FORMULAS = frozenset({"union"})


@dataclass(frozen=True)
class ChiRule:
    rule_id: str
    hazard_ids: tuple[str, str]
    phi_min: dict[str, float]
    formula: str
    formula_version: str
    model_version: str
    compound_hazard_id: str
    notes: str

    def phi_min_for(self, hazard_id: str) -> float:
        if hazard_id not in self.phi_min:
            raise KeyError(f"rule {self.rule_id!r} has no phi_min for {hazard_id!r}")
        return float(self.phi_min[hazard_id])


def _parse_rule(raw: dict[str, Any]) -> ChiRule:
    hazard_ids = tuple(str(h) for h in raw["hazard_ids"])
    if len(hazard_ids) != 2:
        raise ValueError("CHI rules v0.2 support exactly two hazards per rule")
    formula = str(raw.get("formula", "union"))
    if formula not in SUPPORTED_FORMULAS:
        raise ValueError(f"unsupported CHI formula {formula!r}")
    phi_min_raw = raw.get("phi_min") or {}
    if not isinstance(phi_min_raw, dict):
        raise ValueError("phi_min must be a mapping")
    phi_min = {str(k): float(v) for k, v in phi_min_raw.items()}
    for hid in hazard_ids:
        if hid not in phi_min:
            raise ValueError(f"phi_min missing hazard {hid!r} in rule {raw.get('rule_id')}")
    return ChiRule(
        rule_id=str(raw["rule_id"]),
        hazard_ids=(hazard_ids[0], hazard_ids[1]),
        phi_min=phi_min,
        formula=formula,
        formula_version=str(raw["formula_version"]),
        model_version=str(raw["model_version"]),
        compound_hazard_id=str(raw.get("hazard_id") or f"compound/{hazard_ids[0]}-{hazard_ids[1]}"),
        notes=str(raw.get("notes", "")),
    )


def load_rule(rule_id: str) -> ChiRule:
    path = RULES_DIR / f"{rule_id}.yaml"
    if not path.is_file():
        raise KeyError(f"no CHI rule file for rule_id={rule_id!r}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"rule file must be a mapping: {path}")
    rule = _parse_rule(raw)
    if rule.rule_id != rule_id:
        raise ValueError(f"rule_id mismatch in {path.name}")
    return rule


def list_rules() -> tuple[ChiRule, ...]:
    if not RULES_DIR.is_dir():
        return ()
    rules: list[ChiRule] = []
    for path in sorted(RULES_DIR.glob("*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            rules.append(_parse_rule(raw))
    return tuple(rules)
