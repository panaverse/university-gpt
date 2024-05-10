## Quick Guideline to setup locally and Start Development

#### Note: We will use docker compose and devcontainers to setup and run this project locally.

Step 1. Clone the repo
Step 2. In each microservice rename .env.example to env and add any missing env variables only.

Step 3: Now We have 2 compose files to Run the Project

A: docker-compose.yml: Use Compose and then start containers manually in devcontainers (recommended)

- Run `docker compose up --build`
- Using devcontainer remote explorer open each microservice in separate window and run `make dev` or copy dev command from Makefile.

B. Using Compose

You can also spin up everything using the other docker-compose-yml file.

- docker-compose-dev-yaml file

Use it to run compose and everything will be auto started.
`docker compose -f docker-compose-dev.yaml up --build`
NOTE: Review is pending to sync this file with the other compose file

- During Development: We have used the 1st option.

## Run Tests

After setup and getting in devcontainers Open a New Terminal for each microservice and run `pytest` for each micro service

## Frontend:

To Attempt quizzes from Frontend

1. cd quiz-assessment-platform
2. pnpm install
3. pnpm build

## Open Running Microservices in Browser:

- http://localhost:8000/docs
- http://localhost:8001/docs
- http://localhost:8002/docs
- http://localhost:8003/docs
- http://localhost:3000/

The Default Super Admin Credentials are:
- EMAIL: mr.junaid@gmail.com
- PASSWORD: changethis

- PGADMIN: http://localhost:8010/
    Credentials:
      - EMAIL=user@domain.com
      - PASSWORD=SuperSecret

You can change them in user-management/.env file and signup as regular user/student. More SuperAdmins can be added by 1st superadmin only.
