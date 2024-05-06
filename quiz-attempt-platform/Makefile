PATH  := $(PATH)
SHELL := /bin/bash

dev:
	pnpm install && pnpm dev

dep:
	gcloud run deploy uni-frontend --source . --port 3000 --env-vars-file .env.gcp.yaml --allow-unauthenticated --region us-central1 --min-instances 1