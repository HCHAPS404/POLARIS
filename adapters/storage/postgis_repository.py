"""PostGIS-capable SQLAlchemy repository (local dev path)."""

from __future__ import annotations

import os
from typing import Any

from sqlalchemy import create_engine, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from adapters.storage.db.models import AssessmentSnapshotRow, Base, ObservationRow


def database_url_from_env() -> str | None:
    return os.environ.get("POLARIS_DATABASE_URL") or os.environ.get("DATABASE_URL")


class PostgisObservationRepository:
    def __init__(self, url: str, *, create_tables: bool = False) -> None:
        self._url = url
        self._engine: Engine = create_engine(url, pool_pre_ping=True)
        self._session_factory = sessionmaker(bind=self._engine, expire_on_commit=False)
        if create_tables:
            Base.metadata.create_all(self._engine)

    @classmethod
    def from_env(cls, *, create_tables: bool = False) -> PostgisObservationRepository | None:
        url = database_url_from_env()
        if not url:
            return None
        return cls(url, create_tables=create_tables)

    def is_available(self) -> bool:
        try:
            with self._engine.connect() as conn:
                conn.execute(select(1))
            return True
        except Exception:
            return False

    def _session(self) -> Session:
        return self._session_factory()

    def save_observations(self, *, run_id: str, observations: list[dict[str, Any]]) -> int:
        if not observations:
            return 0
        rows = [
            {
                "observation_id": str(item["observation_id"]),
                "run_id": run_id,
                "observed_at": str(item["observed_at"]),
                "observed_property": str(item["observed_property"]),
                "payload": item,
            }
            for item in observations
        ]
        stmt = insert(ObservationRow).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=[ObservationRow.observation_id],
            set_={
                "run_id": stmt.excluded.run_id,
                "observed_at": stmt.excluded.observed_at,
                "observed_property": stmt.excluded.observed_property,
                "payload": stmt.excluded.payload,
            },
        )
        with self._session() as session:
            session.execute(stmt)
            session.commit()
        return len(rows)

    def save_assessment_snapshot(
        self, *, run_id: str, fixture_id: str, snapshot: dict[str, Any]
    ) -> None:
        stmt = insert(AssessmentSnapshotRow).values(
            run_id=run_id,
            fixture_id=fixture_id,
            snapshot=snapshot,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[AssessmentSnapshotRow.run_id],
            set_={
                "fixture_id": stmt.excluded.fixture_id,
                "snapshot": stmt.excluded.snapshot,
            },
        )
        with self._session() as session:
            session.execute(stmt)
            session.commit()

    def list_observations(
        self, *, run_id: str | None = None, limit: int = 500
    ) -> list[dict[str, Any]]:
        with self._session() as session:
            q = select(ObservationRow).limit(limit)
            if run_id is not None:
                q = q.where(ObservationRow.run_id == run_id)
            rows = session.scalars(q).all()
            return [row.payload for row in rows]

    def get_observation(self, observation_id: str) -> dict[str, Any] | None:
        with self._session() as session:
            row = session.get(ObservationRow, observation_id)
            return None if row is None else row.payload

    def get_assessment_snapshot(self, run_id: str) -> dict[str, Any] | None:
        with self._session() as session:
            row = session.get(AssessmentSnapshotRow, run_id)
            return None if row is None else row.snapshot
