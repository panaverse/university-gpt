from fastapi import APIRouter, Depends

from api.auth import authent
from api.quiz.topic import views as topics
from api.quiz.question import views as questions

router = APIRouter(prefix="/v1",)

router.include_router(
    topics.router,
    prefix="/topics",
    tags=["Topics"],
    # dependencies=[Depends(authent)], # Reference to enable after auth2 is implemented
)

router.include_router(
    questions.router,
    prefix="/questions",
    tags=["Questions"],
    # dependencies=[Depends(authent)], # Reference to enable after auth2 is implemented
)