"""Contract files exist (P0 DoD)."""

from pathlib import Path

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
    co = (ROOT / "configs" / "countries" / "co.yaml").read_text(encoding="utf-8")
    assert "INTEGRATION_CASE" in co
    region = (ROOT / "configs" / "regions" / "co-cundinamarca.yaml").read_text(encoding="utf-8")
    assert "INTEGRATION_CASE" in region
