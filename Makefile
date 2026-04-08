.PHONY: init dev migrate test lint format worker import-sample e2e

init:
	cp -n .env.example .env || true
	docker compose build

dev:
	docker compose up web db redis nginx

migrate:
	docker compose run --rm web python manage.py makemigrations
	docker compose run --rm web python manage.py migrate

test:
	docker compose run --rm web pytest

lint:
	docker compose run --rm web ruff check .
	docker compose run --rm web black --check .

format:
	docker compose run --rm web black .
	docker compose run --rm web ruff check . --fix

worker:
	docker compose up worker redis db

import-sample:
	docker compose run --rm web python manage.py import_sample_legacy --fixture fixtures/legacy_sample/cards.json

e2e:
	docker compose run --rm web playwright test
