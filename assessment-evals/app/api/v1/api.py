from fastapi import APIRouter
from app.api.v1.routes import (health, answersheet)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(
    answersheet.router, prefix="/answersheet", tags=["AnswerSheet"]
)