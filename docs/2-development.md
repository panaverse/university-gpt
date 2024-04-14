## Quick Guideline to setup locally and Start Development

#### Note: Follow the 4-development.md to setup and run this project in VS code Dev Containors or using Docker Compose.

If you want to setup project locally on your machine then it's still Valid.

1. Clone the repo
2. Rename .env.example to env and add your env variables. (for database urls remove ?sslmode from the end if present)
3. Run Migrations: `Remove any migration file from alembic>versions folder. Next run these commands

```
alembic revision --autogenerate -m "Add DataLayer v1"

alembic upgrade head
```

Note: When running migrations if you get error `NameError: name 'sqlmodel' is not defined` Open alembic>versions> generated_file and this line at top `import sqlmodel`

3. In Terminal Run `Make quiz` - if you don't have make cli tool then run commands in `Makefile`

```
poetry install

poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
