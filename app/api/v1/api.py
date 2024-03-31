from fastapi import APIRouter, Depends

from app.quiz.topic import views as topics
from app.quiz.question import views as questions
from app.quiz.user import views as users
from app.quiz.quiz import views as quizzes
from app.quiz.answersheet import views as answersheets
# from app.quiz.grade import views as grades

router = APIRouter(prefix="/v1",)

router.include_router(
    topics.router,
    prefix="/topics",
    tags=["Topics"],
)

router.include_router(
    questions.router,
    prefix="/questions",
    tags=["Questions"],
)

router.include_router(
    users.router,
    prefix="/user",
    tags=["User"],
)
router.include_router(
    quizzes.router
)

router.include_router(
    answersheets.router,
    prefix="/answersheet",
    tags=["AnswerSheet"],
)

# router.include_router(
#     grades.router,
#     prefix="/grade",
#     tags=["Grade"],
# )
