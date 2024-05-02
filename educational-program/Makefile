PATH  := $(PATH)
SHELL := /bin/bash

dev:
	alembic upgrade head && python app/init_data.py && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

dev_cont_command:
	poetry install && alembic upgrade head && python app/init_data.py  && python -c 'print(\"CONTAINER STARTED RUN FASTAPI SERVER NOW...\")'

g_deploy:
	gcloud run deploy uni-educational-program --source . --port 8000 --env-vars-file .env.gcp.yaml --allow-unauthenticated --region us-central1 --min-instances 1

