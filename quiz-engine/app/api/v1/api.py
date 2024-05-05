from fastapi import APIRouter
from app.api.v1.routes import (health, topic, content, question, answer, quiz, quiz_question, quiz_setting, wrapper)
from app.settings import GET_CUSTOM_GPT_SPEC
from app.api.deps import GetCurrentAdminDep

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"], include_in_schema=GET_CUSTOM_GPT_SPEC)
api_router.include_router(topic.router, prefix="/topic", tags=["Topic"], dependencies=[GetCurrentAdminDep])
api_router.include_router(content.router, prefix="/topic/content", tags=["Content"], include_in_schema=GET_CUSTOM_GPT_SPEC, dependencies=[GetCurrentAdminDep])
api_router.include_router(question.router, prefix="/question", tags=["Question"], dependencies=[GetCurrentAdminDep])
api_router.include_router(answer.router, prefix="/answer", tags=["Answer"], dependencies=[GetCurrentAdminDep])

api_router.include_router(quiz.router, tags=["Quiz"], prefix="/quiz", dependencies=[GetCurrentAdminDep])
api_router.include_router(quiz_question.router, tags=["QuizQuestion"], prefix="/quiz", dependencies=[GetCurrentAdminDep])
api_router.include_router(quiz_setting.router, tags=["QuizSetting"], prefix="/quiz-setting", dependencies=[GetCurrentAdminDep])
api_router.include_router(wrapper.router, tags=["Wrapper & Runtime Generation APIs"], prefix="/wrapper", include_in_schema=GET_CUSTOM_GPT_SPEC)
