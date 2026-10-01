.PHONY: test lint health scaffold-hazard test-cpp compose-config sim-flood sim-replay sim-iot api db-up db-migrate

PYTHON ?= python3

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .

health:
	$(PYTHON) harness/dev/healthcheck.py

scaffold-hazard:
	@test -n "$(NAME)" || (echo "NAME is required, e.g. make scaffold-hazard NAME=flood"; exit 1)
	$(PYTHON) generators/hazard/scaffold.py --name "$(NAME)"

test-cpp:
	cmake -S . -B build/cpp
	cmake --build build/cpp
	cd build/cpp && ctest --output-on-failure

compose-config:
	docker compose -f docker-compose.yml -f infra/compose/compose.yml config

sim-flood:
	$(PYTHON) -m simulation.python.run --scenario simulation/scenarios/flood-bogota-demo.yaml --seed 42

sim-replay:
	$(PYTHON) -m simulation.python.run --scenario simulation/scenarios/flood-mocoa-2017-replay.yaml --seed 42
	$(PYTHON) -m harness.backtesting.replay --scenario simulation/scenarios/flood-mocoa-2017-replay.yaml --seed 42

sim-iot:
	$(PYTHON) -m simulation.python.iot_run --scenario simulation/scenarios/iot-bogota-demo.yaml --seed 42

api:
	$(PYTHON) -m uvicorn main:app --app-dir platform/api --reload --port 8000

db-up:
	docker compose up -d postgres

db-migrate:
	@test -n "$$POLARIS_DATABASE_URL" || (echo "Set POLARIS_DATABASE_URL (see .env.example)"; exit 1)
	$(PYTHON) -m alembic -c adapters/storage/alembic.ini upgrade head
