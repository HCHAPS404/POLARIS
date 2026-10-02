"""Contract files exist (P0 DoD)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REQUIRED = [
    "README.md",
    "README_ARCHITECTURE.md",
    "README_WORKFLOW.md",
    "README_SIMULATION_ENGINEERING.md",
    "MASTER_CURSOR_PROMPT.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "CODEOWNERS",
    "LICENSE",
    "platform/api/main.py",
    "schemas/openapi.yaml",
    "configs/countries/co.yaml",
    "configs/regions/co-cundinamarca.yaml",
    "configs/sites/co-bogota-demo.yaml",
]


def test_contract_files_present() -> None:
    missing = [rel for rel in REQUIRED if not (ROOT / rel).is_file()]
    assert missing == []


def test_fifteen_integration_countries() -> None:
    countries = list((ROOT / "configs" / "countries").glob("*.yaml"))
    assert len(countries) == 15
    for path in countries:
        text = path.read_text(encoding="utf-8")
        assert "INTEGRATION_CASE" in text
        assert "national_catalog_path:" in text
        assert "integration:" in text
    catalogs = list((ROOT / "configs" / "data" / "catalog").glob("*.yaml"))
    assert len(catalogs) == 15
    regions = list((ROOT / "configs" / "regions").glob("*.yaml"))
    assert len(regions) == 15
    for path in countries:
        profile = yaml.safe_load(path.read_text(encoding="utf-8"))
        site_id = (profile.get("integration") or {}).get("site_id")
        assert site_id
        site_path = ROOT / "configs" / "sites" / f"{site_id}.yaml"
        assert site_path.is_file()
        assert "INTEGRATION_CASE" in site_path.read_text(encoding="utf-8")
        region_id = profile["integration"]["region_id"]
        region_path = ROOT / "configs" / "regions" / f"{region_id}.yaml"
        assert region_path.is_file()
