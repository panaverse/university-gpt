from fastapi import APIRouter, status

from app.api.deps import AsyncSessionDep
from app.core.config import logger_config
from app.crud.health_crud import get_health, get_stats
from app.models.health_model import Health, Stats


router = APIRouter()
logger = logger_config(__name__)


@router.get(
    "",
    response_model=Health,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": Health}},
)
async def health(db: AsyncSessionDep):
    return await get_health(db=db)


@router.get(
    "/stats",
    response_model=Stats,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": Stats}},
)
async def health_stats(db: AsyncSessionDep):
    return await get_stats(db=db)
