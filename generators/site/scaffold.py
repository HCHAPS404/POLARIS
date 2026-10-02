#!/usr/bin/env python3
"""Scaffold a SiteProfile YAML stub under configs/sites/."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from generators._common import ROOT, provenance_json, write  # noqa: E402

SITE_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def scaffold(site_id: str, *, country_iso: str, force: bool) -> list:
    if not SITE_RE.match(site_id):
        raise SystemExit(f"invalid site_id {site_id!r}; use kebab-case")
    iso = country_iso.lower()
    created = []
    site_path = ROOT / "configs" / "sites" / f"{site_id}.yaml"
    if write(
        site_path,
        f"""# SiteProfile — scaffold (not a field pilot)
# Evidence: DESIGNED

country_iso: {iso.upper()}
region_id: {iso}-region-stub
site_id: {site_id}
name: {site_id} (scaffold)
status: INTEGRATION_CASE
evidence: DESIGNED
timezone: UTC
priority_hazards:
  - flood
coordinates:
  lon: 0.0
  lat: 0.0
notes: >
  Scaffolded by generators/site/scaffold.py. Illustrative coordinates only.
""",
        force=force,
    ):
        created.append(site_path)

    prov = ROOT / "configs" / "sites" / f"{site_id}.provenance.json"
    if write(
        prov,
        provenance_json(
            generator="generators/site/scaffold.py",
            entity_id=site_id,
            evidence="DESIGNED",
        ),
        force=force,
    ):
        created.append(prov)
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a site profile")
    parser.add_argument("--id", required=True, dest="site_id")
    parser.add_argument("--country", required=True, dest="country_iso")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    created = scaffold(args.site_id, country_iso=args.country_iso, force=args.force)
    for path in created:
        print(path.relative_to(ROOT))
    if not created:
        print("already exists (pass --force to overwrite)", file=sys.stderr)


if __name__ == "__main__":
    main()
