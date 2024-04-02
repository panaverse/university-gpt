from fastapi import APIRouter
from app.api.v1.routes import (
    users,
    university,
    topic,
    quiz,
    question,
    answersheet,
    health,
)

api_router = APIRouter(prefix="/v1")

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(
    university.router, prefix="/university"
)  # university have separate routers for each, program & courses

api_router.include_router(users.router, prefix="/user", tags=["User"])
api_router.include_router(topic.router, prefix="/topic", tags=["Topic"])
api_router.include_router(question.router, prefix="/question", tags=["Question"])
api_router.include_router(
    quiz.router, prefix="/quiz-engine"
)  # have separate table for quiz, quiz key, quiz question
api_router.include_router(
    answersheet.router, prefix="/answersheet", tags=["AnswerSheet"]
)
