"""POLARIS FastAPI delivery — health + V1 flood vertical slice.

Evidence: GET /health IMPLEMENTED. V1 observation/assessment/alert/map
routes IMPLEMENTED against SIMULATED fixtures. No LIVE adapters. No
OFFICIAL alerts.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
PLATFORM = Path(__file__).resolve().parents[1]
for path in (str(ROOT), str(PLATFORM)):
    if path not in sys.path:
        sys.path.insert(0, path)

from application.flood_assessment import run_flood_slice  # noqa: E402

from adapters.storage.simulated_json import (  # noqa: E402
    FixtureNotFoundError,
    load_simulated_fixture,
)
from domains.common import DISCLAIMER  # noqa: E402

app = FastAPI(
    title="POLARIS API",
    version="0.1.0",
    description=(
        "Decision-support API. V1 flood slice reads SIMULATED fixtures only. "
        "Not an official warning service."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class AssessmentRunRequest(BaseModel):
    seed: int = Field(default=42)
    fixture_id: str = Field(default="flood-bogota-demo")
    data_class: str | None = None


def _slice(seed: int = 42, fixture_id: str = "flood-bogota-demo"):
    try:
        fixture = load_simulated_fixture(fixture_id)
    except FixtureNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return run_flood_slice(fixture, seed=seed)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "polaris",
        "evidence": "IMPLEMENTED",
        "maturity": "V1-flood-vertical-slice",
        "utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


@app.get("/v1/observations")
def list_observations(
    seed: int = Query(default=42),
    fixture_id: str = Query(default="flood-bogota-demo"),
) -> dict:
    result = _slice(seed=seed, fixture_id=fixture_id)
    return {
        "data_class": result.data_class,
        "fixture_id": result.fixture_id,
        "run_id": result.run_id,
        "disclaimer": DISCLAIMER,
        "observations": result.observations(),
    }


@app.get("/v1/observations/{observation_id}")
def get_observation(
    observation_id: str,
    seed: int = Query(default=42),
    fixture_id: str = Query(default="flood-bogota-demo"),
) -> dict:
    result = _slice(seed=seed, fixture_id=fixture_id)
    for item in result.observations():
        if item["observation_id"] == observation_id:
            return item
    raise HTTPException(status_code=404, detail="observation not found")


@app.get("/v1/assessments")
def list_assessments(
    seed: int = Query(default=42),
    fixture_id: str = Query(default="flood-bogota-demo"),
) -> dict:
    return _slice(seed=seed, fixture_id=fixture_id).to_dict()


@app.get("/v1/assessments/{spatial_unit_id}")
def get_assessment(
    spatial_unit_id: str,
    seed: int = Query(default=42),
    fixture_id: str = Query(default="flood-bogota-demo"),
) -> dict:
    result = _slice(seed=seed, fixture_id=fixture_id)
    for unit in result.units:
        if unit.spatial_unit_id == spatial_unit_id:
            return unit.to_dict()
    raise HTTPException(status_code=404, detail="spatial unit not found")


@app.post("/v1/assessments/run")
def run_assessment(payload: AssessmentRunRequest | None = None) -> dict:
    body = payload or AssessmentRunRequest()
    if body.data_class not in (None, "SIMULATED"):
        raise HTTPException(
            status_code=400,
            detail="V1 refuses data_class other than SIMULATED",
        )
    return _slice(seed=body.seed, fixture_id=body.fixture_id).to_dict()


@app.get("/v1/alerts")
def list_alerts(
    seed: int = Query(default=42),
    fixture_id: str = Query(default="flood-bogota-demo"),
) -> dict:
    result = _slice(seed=seed, fixture_id=fixture_id)
    alerts = [unit.alert.to_dict() for unit in result.units]
    if any(item["status"] != "DRAFT" for item in alerts):
        raise HTTPException(status_code=500, detail="non-DRAFT alert blocked")
    return {
        "data_class": result.data_class,
        "run_id": result.run_id,
        "disclaimer": DISCLAIMER,
        "alerts": alerts,
    }


@app.get("/v1/map/geojson")
def map_geojson(
    seed: int = Query(default=42),
    fixture_id: str = Query(default="flood-bogota-demo"),
) -> dict:
    return _slice(seed=seed, fixture_id=fixture_id).to_geojson()


HORIZON = ROOT / "apps" / "horizon-web"
if (HORIZON / "index.html").is_file():
    app.mount("/horizon", StaticFiles(directory=str(HORIZON), html=True), name="horizon")
