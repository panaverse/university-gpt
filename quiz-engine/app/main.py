from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from app import settings
from app.core.config import logger_config
from app.api.v1 import api as v1_api
from app.settings import GET_CUSTOM_GPT_SPEC
logger = logger_config(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup: triggered")
    origins = [str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS]
    print(f"Allowed origins: {origins}")
    yield
    logger.info("shutdown: triggered")

def get_servers():
    if GET_CUSTOM_GPT_SPEC is False:
        return [{"url": "https://bug-accurate-heron.ngrok-free.app", "description": "Dep Test Server"}]
    return [{"url": "http://localhost:8002", "description": "Development Server"},]

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    servers=get_servers(),
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


@app.get(f"{settings.API_V1_STR}/container", tags=["Health"], include_in_schema=GET_CUSTOM_GPT_SPEC)
def read_root():
    return {"Container": "Topic & Question Bank Running", "Port": "8002"}