"""PostGIS repository integration (optional — requires running Postgres)."""

from __future__ import annotations

import os

import pytest

from adapters.storage.postgis_repository import PostgisObservationRepository

pytestmark = pytest.mark.postgis


@pytest.mark.skipif(
    not os.environ.get("POLARIS_DATABASE_URL"),
    reason="POLARIS_DATABASE_URL not set — skip PostGIS integration",
)
def test_postgis_roundtrip() -> None:
    repo = PostgisObservationRepository.from_env(create_tables=True)
    assert repo is not None
    assert repo.is_available()
    run_id = "test-run-postgis"
    obs = [
        {
            "observation_id": "postgis-test-1",
            "observed_at": "2026-10-01T12:00:00Z",
            "observed_property": "rainfall_mm",
            "value": 5.0,
            "unit": "mm",
            "data_class": "SIMULATED",
        }
    ]
    repo.save_observations(run_id=run_id, observations=obs)
    repo.save_assessment_snapshot(run_id=run_id, fixture_id="fx", snapshot={"run_id": run_id})
    listed = repo.list_observations(run_id=run_id)
    assert len(listed) == 1
    assert repo.get_assessment_snapshot(run_id)["run_id"] == run_id
