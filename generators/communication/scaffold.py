#!/usr/bin/env python3
"""Scaffold a communications profile under configs/communications/."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from generators._common import ROOT, provenance_json, write  # noqa: E402

NAME_RE = re.compile(r"^[a-z][a-z0-9_-]*$")


def scaffold(name: str, *, force: bool) -> list:
    if not NAME_RE.match(name):
        raise SystemExit(f"invalid profile name {name!r}; use kebab-case or snake")

    created = []
    path = ROOT / "configs" / "communications" / f"{name}.yaml"
    if write(
        path,
        f"""# Communications profile — scaffold
# Evidence: DESIGNED. Not an operational deployment.

profile_id: {name}
evidence: DESIGNED

lora_subghz:
  frequency_mhz: 868.0
  tx_power_dbm: 14
  rx_sensitivity_dbm: -137
  latency_ms: 120
  packet_loss: 0.0
  notes: Link budget cross-check via simulation/python/rf (SIMULATED FSPL).

mqtt:
  role: device-telemetry
  evidence: DESIGNED

nats:
  role: internal-event-bus
  evidence: DESIGNED
""",
        force=force,
    ):
        created.append(path)

    prov = ROOT / "configs" / "communications" / f"{name}.provenance.json"
    if write(
        prov,
        provenance_json(
            generator="generators/communication/scaffold.py",
            entity_id=name,
            evidence="DESIGNED",
        ),
        force=force,
    ):
        created.append(prov)
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a communications profile")
    parser.add_argument("--name", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    created = scaffold(args.name, force=args.force)
    for path in created:
        print(path.relative_to(ROOT))
    if not created:
        print("already exists (pass --force to overwrite)", file=sys.stderr)


if __name__ == "__main__":
    main()
