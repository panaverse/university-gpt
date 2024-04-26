from fastapi import APIRouter
from app.api.v1.routes import (university, health, program, course)



api_router = APIRouter(prefix="/v1")

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(university.router_uni, prefix="/university", tags=["University"])
api_router.include_router(program.router_prog, prefix="/program", tags=["Program"])
api_router.include_router(course.router_course, prefix="/course", tags=["Course"])