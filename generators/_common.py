"""Shared helpers for POLARIS scaffold generators."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(path: Path, content: str, *, force: bool) -> bool:
    """Write file; return True if created or overwritten."""
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def provenance_json(*, generator: str, entity_id: str, evidence: str) -> str:
    return (
        json.dumps(
            {
                "generator": generator,
                "entity_id": entity_id,
                "utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "evidence": evidence,
            },
            indent=2,
        )
        + "\n"
    )
