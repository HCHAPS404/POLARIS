.PHONY: test lint health scaffold-hazard scaffold-country scaffold-site scaffold-sensor scaffold-communication scaffold-scenario test-cpp test-cpp-bindings compose-config sim-flood sim-replay sim-iot api db-up db-migrate demo up down demo-compose smoke-compose harness-integration harness-simulation harness-faults harness-e2e harness-benchmark

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

scaffold-country:
	@test -n "$(ISO)" || (echo "ISO is required, e.g. make scaffold-country ISO=co"; exit 1)
	$(PYTHON) generators/country/scaffold.py --iso "$(ISO)"

scaffold-site:
	@test -n "$(ID)" || (echo "ID is required"; exit 1)
	@test -n "$(COUNTRY)" || (echo "COUNTRY is required"; exit 1)
	$(PYTHON) generators/site/scaffold.py --id "$(ID)" --country "$(COUNTRY)"

scaffold-sensor:
	@test -n "$(NAME)" || (echo "NAME is required"; exit 1)
	$(PYTHON) generators/sensor/scaffold.py --name "$(NAME)"

scaffold-communication:
	@test -n "$(NAME)" || (echo "NAME is required"; exit 1)
	$(PYTHON) generators/communication/scaffold.py --name "$(NAME)"

scaffold-scenario:
	@test -n "$(NAME)" || (echo "NAME is required"; exit 1)
	$(PYTHON) generators/scenario/scaffold.py --name "$(NAME)" --hazard "$(or $(HAZARD),flood)"

harness-integration:
	$(PYTHON) harness/integration/run_integration.py

harness-simulation:
	$(PYTHON) harness/simulation/run_simulation.py

harness-faults:
	$(PYTHON) harness/fault-injection/run_faults.py

harness-e2e:
	$(PYTHON) harness/e2e/run_e2e.py

harness-benchmark:
	$(PYTHON) harness/benchmark/benchmark_flood.py

test-cpp:
	cmake -S . -B build/cpp
	cmake --build build/cpp
	cd build/cpp && ctest --output-on-failure

test-cpp-bindings:
	cmake -S . -B build/cpp -DBUILD_PYBIND11_BINDINGS=ON
	cmake --build build/cpp
	cd build/cpp && ctest --output-on-failure
	POLARIS_EVENT_SCHEDULER_BUILT=1 PYTHONPATH=build/cpp $(PYTHON) -m pytest tests/unit/test_event_scheduler_binding.py -q

compose-config:
	docker compose -f docker-compose.yml -f infra/compose/compose.yml config

sim-flood:
	$(PYTHON) -m simulation.python.run --scenario simulation/scenarios/flood-bogota-demo.yaml --seed 42

sim-replay:
	$(PYTHON) -m simulation.python.run --scenario simulation/scenarios/flood-mocoa-2017-replay.yaml --seed 42
	$(PYTHON) -m harness.backtesting.replay --scenario simulation/scenarios/flood-mocoa-2017-replay.yaml --seed 42

sim-experiments:
	$(PYTHON) -m backtesting.experiments.run_experiments --seed 42

sim-monte-carlo:
	$(PYTHON) -m harness.backtesting.monte_carlo --seed 42 --draws 200

sim-fault-injection:
	$(PYTHON) -m harness.fault_injection.runner

sim-iot:
	$(PYTHON) -m simulation.python.iot_run --scenario simulation/scenarios/iot-bogota-demo.yaml --seed 42

demo:
	bash harness/demo/run_demo.sh

api:
	$(PYTHON) -m uvicorn main:app --app-dir platform/api --reload --port 8000

db-up:
	docker compose up -d postgres

db-migrate:
	@test -n "$$POLARIS_DATABASE_URL" || (echo "Set POLARIS_DATABASE_URL (see .env.example)"; exit 1)
	$(PYTHON) -m alembic -c adapters/storage/alembic.ini upgrade head

up:
	docker compose up --build -d

down:
	docker compose down

demo-compose:
	docker compose exec -T api make demo

smoke-compose:
	bash harness/dev/smoke_compose.sh
