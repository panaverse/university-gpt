PATH  := $(PATH)
SHELL := /bin/bash

dev:
	alembic upgrade head && python app/init_data.py && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

dev_cont_command:
	poetry install && alembic upgrade head && python app/init_data.py  && python -c 'print(\"CONTAINER STARTED RUN FASTAPI SERVER NOW...\")'