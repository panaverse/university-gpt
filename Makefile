PATH  := $(PATH)
SHELL := /bin/bash

run_quiz:
	poetry install && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000

dev_quiz:
	poetry install && poetry run python app/init_data.py && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate:
	poetry run alembic revision --autogenerate -m "Add DataLayer v1"

upgrade:
	poetry run alembic upgrade head
