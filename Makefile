.PHONY: test lint health scaffold-hazard test-cpp compose-config

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
