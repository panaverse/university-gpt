PATH  := $(PATH)
SHELL := /bin/bash

dev:
	poetry install && alembic upgrade head && python app/init_data.py && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

dep:
	gcloud run deploy uni-asses-evals --source . --port 8003 --env-vars-file .env.gcp.yaml --allow-unauthenticated --region us-central1 --min-instances 1