# Local Setup & Development Guide

We have following options to setup and run this project locally:
1. On Local Machine
2. Using Docker Compose
3. Using VSCode Dev Containers

We will be using VS Code Dev Containers methods to setup the project locally.

Next we will setup Custom GPT to assist Instructors/Admin following the guidelines in custom-gpt folder

## Requirements:
1. [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. [Review This VSCode DevContainers Step](https://github.com/panaverse/learn-generative-ai/tree/main/05_microservices_all_in_one_platform/14_docker/03_dev_containers)

## Setup Instructions

1. Clone This Repo
2. Rename .env.example to .env(don;t change anything inside it)
3. Open Docker
4. In VS Code
    - press MAC USERs(CMD + Shift + P) & WINDOW USERs (Ctril + Shift + P).
    - search `Dev Containers: Open Folder in Container...`
    - select repo directory/folder
5. Wait for a few seconds and then open in Browser `http://localhost:8000`

Run the Health Endpoints - your development Database is already seeded.

## Run Tests

Open a New Terminal and run `make test` or `poetry run python app/pre_start_tests.py && poetry run pytest`. For tests we have a seperate database.

## Custom GPT
Now setup Custom GPT that will assist Instructors/Admin following the guidelines in custom-gpt folder

Demo Chat: https://chat.openai.com/share/1a330b4f-f872-422e-93d6-52258a43a122

## Containers Architecture & Project Details

A. We are running 3 Containers

1. QuizAPI/DevContainer - This is our FastAPI server for the Quiz API
2. Development Postgres Database Instance
3. Testing Postgres Database Instance

B. For Database config we have used

1. SQLAlchemy ASYNC Engine (To get async engine)
2. SQLModel Async Session (To use Latest SQLModel Query Schema & Features)

Checkout the 1.async-engine.md for more details about it.
