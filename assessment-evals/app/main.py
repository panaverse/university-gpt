from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from app import settings
from app.core.config import logger_config
from app.api.v1 import api as v1_api

logger = logger_config(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup: triggered")
    origins = [str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS]
    print(f"Allowed origins: {origins}")
    yield
    logger.info("shutdown: triggered")


app = FastAPI()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    # servers=[{"url": "http://localhost:8000", "description": "Development Server"}],
)

app.include_router(v1_api.api_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get(f"{settings.API_V1_STR}/container", tags=["Health"])
def read_root():
    return {"Container Running": "Assessment Evals", "Port": "8004"}