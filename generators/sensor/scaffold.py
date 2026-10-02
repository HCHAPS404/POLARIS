#!/usr/bin/env python3
"""Scaffold a logical device YAML under configs/devices/."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from generators._common import ROOT, provenance_json, write  # noqa: E402

NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def scaffold(name: str, *, device_type: str | None, force: bool) -> list:
    if not NAME_RE.match(name):
        raise SystemExit(f"invalid device name {name!r}; use kebab-case")
    dtype = device_type or name
    created = []
    path = ROOT / "configs" / "devices" / f"{name}.yaml"
    if write(
        path,
        f"""# Logical device — scaffold
device_type: {dtype}
schema_version: "devices.v0.1.0"
description: >-
  Scaffolded device profile. SIMULATED only — not a production PCB.

sample_interval_s: 600
calibration_version: "cal.stub.v0.1.0"

sensors:
  - id: primary
    observed_property: placeholder
    unit: "1"
    interface: simulated

communication_profile:
  radio: lora_subghz
  role: end_device
  max_payload_bytes: 51
""",
        force=force,
    ):
        created.append(path)

    prov = ROOT / "configs" / "devices" / f"{name}.provenance.json"
    if write(
        prov,
        provenance_json(
            generator="generators/sensor/scaffold.py",
            entity_id=name,
            evidence="DESIGNED",
        ),
        force=force,
    ):
        created.append(prov)
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a device profile")
    parser.add_argument("--name", required=True)
    parser.add_argument("--device-type", default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    created = scaffold(args.name, device_type=args.device_type, force=args.force)
    for path in created:
        print(path.relative_to(ROOT))
    if not created:
        print("already exists (pass --force to overwrite)", file=sys.stderr)


if __name__ == "__main__":
    main()
