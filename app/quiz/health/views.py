from fastapi import APIRouter, Depends, status
from typing import Annotated

from app.core.database import AsyncSession, get_session
from app.quiz.health.crud import get_health, get_stats
from app.quiz.health.models import Health, Stats
from app.core.utils.logger import logger_config

router = APIRouter()
logger = logger_config(__name__)


@router.get(
    "",
    response_model=Health,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": Health}},
)
async def health(db: Annotated[AsyncSession, Depends(get_session)]):
    return await get_health(db=db)


@router.get(
    "/stats",
    response_model=Stats,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": Stats}},
)
async def health_stats(db: Annotated[AsyncSession, Depends(get_session)]):
    return await get_stats(db=db)
