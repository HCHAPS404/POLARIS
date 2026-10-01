"""POLARIS FastAPI delivery — P0 health only.

Evidence: GET /health is IMPLEMENTED. All other routes are DESIGNED / absent.
"""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import FastAPI

app = FastAPI(
    title="POLARIS API",
    version="0.0.1",
    description="Decision-support API. P0 implements GET /health only.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "polaris",
        "evidence": "IMPLEMENTED",
        "maturity": "P0-foundation",
        "utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
