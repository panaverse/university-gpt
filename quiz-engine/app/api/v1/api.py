from fastapi import APIRouter
from app.api.v1.routes import (health, topic, content, question, answer, quiz, quiz_question, quiz_setting)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(topic.router, prefix="/topic", tags=["Topic"])
api_router.include_router(content.router, prefix="/topic/content", tags=["Content"])
api_router.include_router(question.router, prefix="/question", tags=["Question"])
api_router.include_router(answer.router, prefix="/answer", tags=["Answer"])

api_router.include_router(quiz.router, tags=["Quiz"], prefix="/quiz")
api_router.include_router(quiz_question.router, tags=["QuizQuestion"], prefix="/quiz")
api_router.include_router(quiz_setting.router, tags=["QuizSetting"], prefix="/quiz-setting")
