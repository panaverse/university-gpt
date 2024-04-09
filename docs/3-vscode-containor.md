Now we are using VS Dev Containers for Local Development & Tests.

Understand the basics about them from this step:

https://github.com/panaverse/learn-generative-ai/tree/main/05_microservices_all_in_one_platform/14_docker/03_dev_containers

Firstly follow 2-development.md to clone and setup the project locally.

Then you can simple this folder in VS Code Dev containor the build will complete and then run these commands to ensure everything is working:
1. `make dev`
2. `make test`

Now open the Dockerfile.dev and review it. Next do it for docker-compose.yml file and the same for .devcontainer/devcontainer.json.

Note: If you don't want to use vs code devcontainor then you can simply run it with docker compose as well.

Future TODOS:
1. update .devcontainor.json to configure local git
2. add essential vs code extensions in it as well.
