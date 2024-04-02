PATH  := $(PATH)
SHELL := /bin/bash

quiz:
	poetry install && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
