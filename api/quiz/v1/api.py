from fastapi import APIRouter, Depends

from api.auth import authent
from api.quiz.topic import views as topics
from api.quiz.question import views as questions
from api.quiz.user import views as users
from api.quiz.quiz import views as quizzes
from api.quiz.answersheet import views as answersheets

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

router.include_router(
    users.router,
    prefix="/user",
    tags=["User"],
    # dependencies=[Depends(authent)], # Reference to enable after auth2 is implemented
)
router.include_router(
    quizzes.router,
    prefix="/quiz",
    tags=["Quiz"],
    # dependencies=[Depends(authent)], # Reference to enable after auth2 is implemented
)

router.include_router(
    answersheets.router,
    prefix="/answersheet",
    tags=["AnswerSheet"],
    # dependencies=[Depends(authent)], # Reference to enable after auth2 is implemented
)