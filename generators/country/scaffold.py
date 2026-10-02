#!/usr/bin/env python3
"""Scaffold a CountryProfile YAML stub under configs/countries/."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from generators._common import ROOT, provenance_json, write  # noqa: E402

ISO_RE = re.compile(r"^[a-z]{2}$")


def scaffold(iso_code: str, *, name: str | None, force: bool) -> list:
    iso = iso_code.lower()
    if not ISO_RE.match(iso):
        raise SystemExit(f"invalid iso_code {iso_code!r}; use two letters, e.g. co")

    display = name or iso.upper()
    created = []
    country_path = ROOT / "configs" / "countries" / f"{iso}.yaml"
    if write(
        country_path,
        f"""# CountryProfile stub — scaffold
# Evidence: DESIGNED. Not a live integration. Not a pilot.
iso_code: {iso.upper()}
name: {display}
status: INTEGRATION_CASE
evidence: DESIGNED
timezone: UTC
priority_hazards:
  - flood
notes: >
  Scaffolded by generators/country/scaffold.py. Integration shape only.
""",
        force=force,
    ):
        created.append(country_path)

    prov = ROOT / "configs" / "countries" / f"{iso}.provenance.json"
    if write(
        prov,
        provenance_json(
            generator="generators/country/scaffold.py",
            entity_id=iso,
            evidence="DESIGNED",
        ),
        force=force,
    ):
        created.append(prov)
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a country profile")
    parser.add_argument("--iso", required=True, help="ISO 3166-1 alpha-2, e.g. co")
    parser.add_argument("--name", default=None, help="Display name")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    created = scaffold(args.iso, name=args.name, force=args.force)
    for path in created:
        print(path.relative_to(ROOT))
    if not created:
        print("already exists (pass --force to overwrite)", file=sys.stderr)


if __name__ == "__main__":
    main()
