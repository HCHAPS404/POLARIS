"""CAP-shaped DRAFT/SIMULATION payloads — NOT OFFICIAL CAP distribution."""

from __future__ import annotations

from typing import Any
from xml.etree.ElementTree import Element, SubElement, tostring

from domains.alerting.draft import DraftAlert
from domains.common import DISCLAIMER

CAP_FORMULA_VERSION = "alert.cap-draft.v0.1.0"
CAP_STATUS = "DRAFT"
CAP_MSG_TYPE = "Alert"
CAP_SCOPE = "Public"
CAP_CATEGORY = "Geo"
CAP_URGENCY = "Unknown"
CAP_SEVERITY_MAP = {
    "info": "Minor",
    "watch": "Moderate",
    "warning": "Severe",
    "proposed": "Extreme",
}


def _cap_headline(alert: DraftAlert) -> str:
    hazard = alert.hazard_id or "hazard"
    return (
        f"[DRAFT/SIMULATION] {hazard} decision-support — level {alert.level} "
        f"(NOT an official CAP alert)"
    )


def draft_alert_to_cap_json(alert: DraftAlert) -> dict[str, Any]:
    if alert.status != CAP_STATUS:
        raise ValueError("CAP export requires DRAFT status")
    return {
        "cap_schema": "polaris-cap-draft-json.v0.1.0",
        "formula_version": CAP_FORMULA_VERSION,
        "status": CAP_STATUS,
        "msgType": CAP_MSG_TYPE,
        "scope": CAP_SCOPE,
        "category": CAP_CATEGORY,
        "urgency": CAP_URGENCY,
        "severity": CAP_SEVERITY_MAP.get(alert.level, "Unknown"),
        "event": alert.hazard_id,
        "headline": _cap_headline(alert),
        "description": DISCLAIMER,
        "instruction": "Human operator review required before any operational use.",
        "identifier": alert.alert_id,
        "sender": "polaris:simulation",
        "sent": alert.provenance.get("computed_at"),
        "source": "POLARIS decision-support (SIMULATED/DRAFT)",
        "info": {
            "language": "es-CO",
            "area": {
                "areaDesc": alert.spatial_unit_id,
                "polygon": None,
            },
            "parameter": [
                {"name": "operational_risk", "value": str(alert.operational_risk_value)},
                {"name": "polaris_level", "value": alert.level},
            ],
        },
        "official": False,
        "human_in_the_loop": True,
        "disclaimer": DISCLAIMER,
    }


def draft_alert_to_cap_xml(alert: DraftAlert) -> str:
    root = Element("alert")
    root.set("xmlns", "urn:oasis:names:tc:emergency:cap:1.2")
    SubElement(root, "identifier").text = alert.alert_id
    SubElement(root, "sender").text = "polaris:simulation"
    SubElement(root, "sent").text = str(alert.provenance.get("computed_at") or "")
    SubElement(root, "status").text = "Test"
    SubElement(root, "msgType").text = CAP_MSG_TYPE
    SubElement(root, "scope").text = CAP_SCOPE
    info = SubElement(root, "info")
    SubElement(info, "category").text = CAP_CATEGORY
    SubElement(info, "event").text = str(alert.hazard_id or "hazard")
    SubElement(info, "urgency").text = CAP_URGENCY
    SubElement(info, "severity").text = CAP_SEVERITY_MAP.get(alert.level, "Unknown")
    SubElement(info, "headline").text = _cap_headline(alert)
    SubElement(info, "description").text = DISCLAIMER
    SubElement(info, "instruction").text = "DRAFT/SIMULATION — HITL required."
    area = SubElement(info, "area")
    SubElement(area, "areaDesc").text = alert.spatial_unit_id
    note = SubElement(root, "note")
    note.text = (
        "POLARIS CAP XML is DRAFT/SIMULATION only; status=Test; "
        "not for public distribution."
    )
    return tostring(root, encoding="unicode")


def cap_bundle_for_alert(alert: DraftAlert, *, fmt: str) -> dict[str, Any]:
    fmt_norm = fmt.lower()
    if fmt_norm == "json":
        return {
            "format": "cap-json",
            "cap": draft_alert_to_cap_json(alert),
            "disclaimer": DISCLAIMER,
        }
    if fmt_norm == "xml":
        return {
            "format": "cap-xml",
            "cap_xml": draft_alert_to_cap_xml(alert),
            "disclaimer": DISCLAIMER,
        }
    if fmt_norm in ("both", "cap"):
        return {
            "format": "cap",
            "cap": draft_alert_to_cap_json(alert),
            "cap_xml": draft_alert_to_cap_xml(alert),
            "disclaimer": DISCLAIMER,
        }
    raise ValueError(f"unsupported CAP format {fmt!r}")
