PYTHON ?= python3
VENV ?= .venv
ACTIVATE = . $(VENV)/bin/activate

.PHONY: setup run-api docker-up docker-down eval lint test

setup:
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pip install -r requirements.txt

run-api:
	$(ACTIVATE) && uvicorn apps.api.main:app --reload --port 8000

docker-up:
	docker compose up -d

docker-down:
	docker compose down

eval:
	$(ACTIVATE) && python -m ml.evaluation.run --config configs/config.yaml

lint:
	$(ACTIVATE) && ruff .
	$(ACTIVATE) && black --check .
	$(ACTIVATE) && mypy .

test:
	$(ACTIVATE) && pytest -q
