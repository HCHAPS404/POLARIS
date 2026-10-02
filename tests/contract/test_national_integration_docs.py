"""Contract: country one-pagers exist for all integration territories."""

from __future__ import annotations

from pathlib import Path

from adapters.data.national.registry import list_integration_country_codes

ROOT = Path(__file__).resolve().parents[2]


def test_country_one_pagers() -> None:
    for iso in list_integration_country_codes():
        path = ROOT / "docs" / "countries" / f"{iso.lower()}.md"
        assert path.is_file(), f"missing one-pager: {path}"
        text = path.read_text(encoding="utf-8")
        assert "INTEGRATION CASE" in text
        assert iso in text
