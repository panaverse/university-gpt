from fastapi import APIRouter

from api.auth import authent
from api.quiz.v1 import api as quiz
from api.quiz.health import views as health
from api.quiz.university import views as university_manager

api = APIRouter(prefix="/quiz/api",)


api.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
    # dependencies=[Depends(authent)], # Reference to enable after auth2 is implemented
)
api.include_router(
    quiz.router,
)
api.include_router(
    university_manager.router,
    # dependencies=[Depends(authent)], # Reference to enable after auth2 is implemented
)