## Quick Guideline to setup locally and Start Development

#### Note: We will use docker compose and devcontainers to setup and run this project locally.

1. Clone the repo
2. In each microservice rename .env.example to env and add any missing env variables only. 

Now We have 2 options to Run the Project

A: docker-compose.yml: Use Compose and then start containers manually in devcontainers (recommended)

- Run docker compose up --build
- Using devcontainer remote explrer open each microservice in seperate window and run `make dev` or copy dev comand from Makefile. 

B. Using Compose

You can also spin up everything using the other docker-compose-yml file.

- docker-compose-dev-yaml file

Use it to run compose and everything will be auto started.
NOTE: Review is pending to sync this file with the other compose file

- During Development: We have used the 1st option.

## Run Tests

After setup and getting in devcontainers Open a New Terminal for each microservice and run `pytest` for each micro service

## Frontend:

To Attempt quizzes from Frontend

1. cd quiz-assessment-platform
2. pnpm install
3. pnpm build

