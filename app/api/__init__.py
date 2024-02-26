from fastapi import APIRouter

from app.api.v1 import api as quiz
from app.quiz.health import views as health
from app.quiz.university import views as university_manager

api = APIRouter(prefix="/quiz/api",)


api.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)
api.include_router(
    quiz.router,
)
api.include_router(
    university_manager.router,
)