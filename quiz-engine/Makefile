PATH  := $(PATH)
SHELL := /bin/bash

dev:
	poetry install && alembic upgrade head && python app/init_data.py && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

dep:
	gcloud run deploy uni-quiz-engine --source . --port 8000 --env-vars-file .env.gcp.yaml --allow-unauthenticated --region us-central1 --min-instances 1