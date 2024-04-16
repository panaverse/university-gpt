PATH  := $(PATH)
SHELL := /bin/bash

compose:
	docker-compose -f docker-compose-dev.yml up

compose-name:
	docker-compose ps

compose-d:
	docker-compose down

compose-b:
	docker-compose  -f docker-compose-dev.yml up --build

compose-in:
	docker-compose exec devcontainor /bin/bash

dev:
	poetry install && poetry run python app/init_data.py && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate:
	poetry run alembic revision --autogenerate -m "Add DataLayer v1"

upgrade:
	poetry run alembic upgrade head

test:
	poetry install && poetry run python app/pre_start_tests.py && poetry run pytest

build:
	 docker build -f Dockerfile.dev -t quiz-api .

run:
	docker run -d --name quiz-api -v /Users/mjs/Documents/GitHub/panaverse-official/university-gpt:/code -p 8000:8000 --env-file .env quiz-api

doc-test:
	docker run -it --rm quiz-api /bin/bash -c "poetry run pytest"
