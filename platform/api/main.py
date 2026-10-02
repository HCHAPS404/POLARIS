"""POLARIS FastAPI delivery — health + flood slice + historical replay.

Evidence: GET /health IMPLEMENTED. Observation/assessment/alert/map
routes IMPLEMENTED against SIMULATED and HISTORICAL_REPLAY fixtures.
No LIVE adapters. No OFFICIAL alerts.
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

from application.iot_ingest import ingest_iot_scenario  # noqa: E402
from application.live_ingest import ingest_live_precipitation  # noqa: E402

from adapters.storage.repository_factory import get_observation_repository  # noqa: E402
from adapters.storage.simulated_json import (  # noqa: E402
    FixtureNotFoundError,
    load_fixture,
)
from domains.common import ALLOWED_DATA_CLASSES, DATA_CLASS_LIVE, DISCLAIMER  # noqa: E402
from domains.hazards.registry import run_hazard_slice  # noqa: E402

app = FastAPI(
    title="POLARIS API",
    version="0.1.0",
    description=(
        "Decision-support API. Flood slice reads SIMULATED or HISTORICAL_REPLAY "
        "fixtures. Not an official warning service."
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


class IoTIngestRequest(BaseModel):
    seed: int = Field(default=42)
    scenario_id: str = Field(default="iot-bogota-demo")


class LivePrecipIngestRequest(BaseModel):
    site_id: str = Field(default="co-bogota-demo")
    seed: int = Field(default=42)


def _slice(seed: int = 42, fixture_id: str = "flood-bogota-demo"):
    try:
        fixture = load_fixture(fixture_id)
    except FixtureNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return run_hazard_slice(fixture, seed=seed)


def _refuse_live(data_class: str | None) -> None:
    if data_class == DATA_CLASS_LIVE:
        raise HTTPException(status_code=400, detail="LIVE is refused (not faked)")
    if data_class not in (None, *ALLOWED_DATA_CLASSES):
        raise HTTPException(
            status_code=400,
            detail="data_class must be SIMULATED or HISTORICAL_REPLAY",
        )


@app.get("/health")
def health() -> dict[str, str]:
    repo = get_observation_repository()
    from adapters.storage.postgis_repository import PostgisObservationRepository

    storage = (
        "postgis"
        if isinstance(repo, PostgisObservationRepository) and repo.is_available()
        else "memory"
    )
    return {
        "status": "ok",
        "service": "polaris",
        "evidence": "IMPLEMENTED",
        "maturity": "v1.0.0-response-quest",
        "storage_backend": storage,
        "utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


@app.get("/v1/observations")
def list_observations(
    seed: int = Query(default=42),
    fixture_id: str = Query(default="flood-bogota-demo"),
    run_id: str | None = Query(default=None),
) -> dict:
    if run_id:
        repo = get_observation_repository()
        stored = repo.list_observations(run_id=run_id)
        if stored:
            snap = repo.get_assessment_snapshot(run_id)
            data_class = (
                str(snap.get("data_class")) if snap else stored[0].get("data_class", "SIMULATED")
            )
            return {
                "data_class": data_class,
                "run_id": run_id,
                "disclaimer": DISCLAIMER,
                "storage_backend": "postgis"
                if repo.__class__.__name__ == "PostgisObservationRepository"
                else "memory",
                "observations": stored,
            }
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
    run_id: str | None = Query(default=None),
) -> dict:
    if run_id:
        repo = get_observation_repository()
        snap = repo.get_assessment_snapshot(run_id)
        if snap:
            return snap
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
    _refuse_live(body.data_class)
    result = _slice(seed=body.seed, fixture_id=body.fixture_id)
    if body.data_class is not None and body.data_class != result.data_class:
        raise HTTPException(
            status_code=400,
            detail="requested data_class does not match fixture",
        )
    return result.to_dict()


@app.get("/v1/alerts")
def list_alerts(
    seed: int = Query(default=42),
    fixture_id: str = Query(default="flood-bogota-demo"),
    format: str | None = Query(default=None, alias="format"),
) -> dict:
    from domains.alerting.cap_draft import cap_bundle_for_alert

    result = _slice(seed=seed, fixture_id=fixture_id)
    alerts = [unit.alert.to_dict() for unit in result.units]
    if any(item["status"] != "DRAFT" for item in alerts):
        raise HTTPException(status_code=500, detail="non-DRAFT alert blocked")
    payload: dict = {
        "data_class": result.data_class,
        "run_id": result.run_id,
        "disclaimer": DISCLAIMER,
        "alerts": alerts,
    }
    if format and format.lower() in ("cap", "json", "xml", "both"):
        fmt = format.lower()
        payload["cap_alerts"] = [
            cap_bundle_for_alert(unit.alert, fmt=fmt) for unit in result.units
        ]
    return payload


@app.get("/v1/map/geojson")
def map_geojson(
    seed: int = Query(default=42),
    fixture_id: str = Query(default="flood-bogota-demo"),
) -> dict:
    return _slice(seed=seed, fixture_id=fixture_id).to_geojson()


@app.post("/v1/ingest/live/precipitation")
def ingest_live_precip(payload: LivePrecipIngestRequest | None = None) -> dict:
    body = payload or LivePrecipIngestRequest()
    return ingest_live_precipitation(site_id=body.site_id, seed=body.seed)


@app.post("/v1/ingest/iot")
def ingest_iot(payload: IoTIngestRequest | None = None) -> dict:
    body = payload or IoTIngestRequest()
    try:
        return ingest_iot_scenario(scenario_id=body.scenario_id, seed=body.seed)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/v1/compound/sites")
def list_compound_sites() -> dict:
    from domains.compound.site_pairs import list_compound_sites

    sites = list_compound_sites()
    return {
        "disclaimer": DISCLAIMER,
        "sites": [
            {
                "site_id": s.site_id,
                "flood_fixture_id": s.flood_fixture_id,
                "landslide_fixture_id": s.landslide_fixture_id,
                "evidence": s.evidence,
                "notes": s.notes,
            }
            for s in sites
        ],
    }


@app.get("/v1/compound/chi")
def get_compound_chi(
    site_id: str = Query(default="co-bogota-demo"),
    seed: int = Query(default=42),
) -> dict:
    from application.compound_assessment import run_compound_chi

    try:
        return run_compound_chi(site_id=site_id, seed=seed).to_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/v1/backtests/{scenario_id}")
def get_backtest(
    scenario_id: str,
    seed: int = Query(default=42),
) -> dict:
    from harness.backtesting.replay import run_backtest

    scenario = ROOT / "simulation" / "scenarios" / f"{scenario_id}.yaml"
    if not scenario.is_file():
        raise HTTPException(status_code=404, detail="scenario not found")
    try:
        return run_backtest(scenario, seed)
    except SystemExit as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


HORIZON = ROOT / "apps" / "horizon-web"
if (HORIZON / "index.html").is_file():
    app.mount("/horizon", StaticFiles(directory=str(HORIZON), html=True), name="horizon")

VECTOR = ROOT / "apps" / "vector-console"
if (VECTOR / "index.html").is_file():
    app.mount("/vector", StaticFiles(directory=str(VECTOR), html=True), name="vector")

FORGE = ROOT / "apps" / "forge-studio"
if (FORGE / "index.html").is_file():
    app.mount("/forge", StaticFiles(directory=str(FORGE), html=True), name="forge")
