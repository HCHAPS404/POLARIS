"""Scaffold generators create real config/scenario files."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from generators.communication.scaffold import scaffold as scaffold_comm  # noqa: E402
from generators.country.scaffold import scaffold as scaffold_country  # noqa: E402
from generators.scenario.scaffold import scaffold as scaffold_scenario  # noqa: E402
from generators.sensor.scaffold import scaffold as scaffold_sensor  # noqa: E402
from generators.site.scaffold import scaffold as scaffold_site  # noqa: E402


def test_scaffold_country_site_sensor_comm_scenario() -> None:
    iso = "zz"
    site = "zz-scaffold-demo"
    device = "zz-scaffold-device"
    comm = "zz_scaffold_comm"
    scenario = "zz-scaffold-scenario"
    paths = []
    try:
        paths.extend(scaffold_country(iso, name="Scaffold", force=True))
        paths.extend(scaffold_site(site, country_iso=iso, force=True))
        paths.extend(scaffold_sensor(device, device_type="zz-type", force=True))
        paths.extend(scaffold_comm(comm, force=True))
        paths.extend(scaffold_scenario(scenario, hazard_id="flood", force=True))
        assert (ROOT / "configs" / "countries" / f"{iso}.yaml").is_file()
        assert (ROOT / "configs" / "sites" / f"{site}.yaml").is_file()
        assert (ROOT / "configs" / "devices" / f"{device}.yaml").is_file()
        assert (ROOT / "configs" / "communications" / f"{comm}.yaml").is_file()
        assert (ROOT / "simulation" / "scenarios" / f"{scenario}.yaml").is_file()
    finally:
        for rel in (
            f"configs/countries/{iso}.yaml",
            f"configs/countries/{iso}.provenance.json",
            f"configs/sites/{site}.yaml",
            f"configs/sites/{site}.provenance.json",
            f"configs/devices/{device}.yaml",
            f"configs/devices/{device}.provenance.json",
            f"configs/communications/{comm}.yaml",
            f"configs/communications/{comm}.provenance.json",
            f"simulation/scenarios/{scenario}.yaml",
            f"simulation/scenarios/{scenario}.provenance.json",
        ):
            p = ROOT / rel
            if p.exists():
                p.unlink()
