#!/usr/bin/env bash
# Wait for PostGIS, run Alembic, start uvicorn. Dev/demo only — not production HA.
set -euo pipefail

cd /app

if [[ -z "${POLARIS_DATABASE_URL:-}" ]]; then
  echo "POLARIS_DATABASE_URL is required inside compose (see .env.example)."
  exit 1
fi

echo "Waiting for PostgreSQL…"
python3 <<'PY'
import os
import sys
import time

import psycopg

url = os.environ["POLARIS_DATABASE_URL"]
# SQLAlchemy-style URL → psycopg conninfo
conninfo = url.replace("postgresql+psycopg://", "postgresql://", 1)

for attempt in range(60):
    try:
        with psycopg.connect(conninfo, connect_timeout=3):
            print("PostgreSQL is ready.")
            sys.exit(0)
    except Exception as exc:
        print(f"  attempt {attempt + 1}/60: {exc}", flush=True)
        time.sleep(2)
print("PostgreSQL did not become ready in time.", file=sys.stderr)
sys.exit(1)
PY

echo "Running Alembic migrations…"
python3 -m alembic -c adapters/storage/alembic.ini upgrade head

echo "Starting POLARIS API on :8000…"
exec python3 -m uvicorn main:app --app-dir platform/api --host 0.0.0.0 --port 8000
