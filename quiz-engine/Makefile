PATH  := $(PATH)
SHELL := /bin/bash

dev:
	alembic upgrade head && python app/init_data.py && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload