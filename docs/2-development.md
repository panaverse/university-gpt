## Quick Guideline to setup locally and Start Development

1. Clone the repo
2. Rename .env.example to env and add your env variables. (for database urls remove ?sslmode from the end if present)
3. Run Migrations: `Remove any migration file from alembic>versions folder. Next run these commands

```
alembic revision --autogenerate -m "Add DataLayer v1"

alembic upgrade head
```

3. In Terminal Run `Make quiz` - if you don't have make cli tool then run commands in `Makefile`

```
poetry install

poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
