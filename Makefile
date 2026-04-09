.PHONY: init dev migrate test lint format worker import-sample e2e seed

init:
	@if [ ! -f .env ]; then cp .env.example .env; fi
	docker compose build

dev:
	docker compose up --build

migrate:
	docker compose run --rm web python app/manage.py migrate

test:
	docker compose run --rm web pytest

lint:
	docker compose run --rm web ruff check .
	docker compose run --rm web black --check .
	docker compose run --rm web mypy app

format:
	docker compose run --rm web black .
	docker compose run --rm web ruff check --fix .

worker:
	docker compose up worker

import-sample:
	docker compose run --rm web python app/manage.py import_sample_fixture

seed:
	docker compose run --rm web python app/manage.py seed_demo

e2e:
	docker compose run --rm web pytest tests/e2e
