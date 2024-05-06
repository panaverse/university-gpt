PATH  := $(PATH)
SHELL := /bin/bash

dev:
	poetry install && python app/initial_data.py && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload


dep:
	gcloud run deploy uni-user-management --source . --port 8000 --env-vars-file .env.gcp.yaml --allow-unauthenticated --region us-central1 --min-instances 1