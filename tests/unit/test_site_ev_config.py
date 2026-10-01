"""Site exposure/vulnerability config resolver."""

from __future__ import annotations

from domains.sites.ev_config import resolve_exposure, resolve_vulnerability


def test_bogota_demo_uses_site_yaml() -> None:
    exposure = resolve_exposure(site_id="co-bogota-demo", spatial_unit_id="co-bogota-demo-center")
    vuln = resolve_vulnerability(site_id="co-bogota-demo", spatial_unit_id="co-bogota-demo-center")
    assert exposure.value == 0.70
    assert vuln.value == 0.55
    assert exposure.evidence == "EXPERIMENTAL"
    assert exposure.formula_version == "exposure.site-config.v0.1.0"


def test_unknown_unit_falls_back_to_stub() -> None:
    exposure = resolve_exposure(site_id="co-bogota-demo", spatial_unit_id="unknown-unit")
    assert exposure.evidence == "PLACEHOLDER"
