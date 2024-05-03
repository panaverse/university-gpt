## Quick Guideline to setup locally and Start Development

#### Note: Follow the 4-development.md to setup and run this project in VS code Dev Containors or using Docker Compose.

If you want to setup project locally on your machine then it's still Valid.

1. Clone the repo
2. In each microservice rename .env.example to env and add your env variables. 

3. We have 2 options to Run the Project

A: docker-compose.yml Use Compose with Sleep Command and then start containers

- Run docker compose up --build
- Using devcontainer open each microservice in seperate window and run `make dev` or copy dev comand from Makefile. 

B. Using Compose

- docker-compose-dev-yaml file

Use it to run compose and everything will be auto started.
NOTE: Review is pending to sync this file with the other compose file

- During Development: We have used the 1st option.

## Run Tests

Open a New Terminal and run `pytest` for each micro service
