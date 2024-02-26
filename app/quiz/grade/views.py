from fastapi import APIRouter, Depends, status
from typing import Annotated

from app.core.database import AsyncSession, get_session
from app.quiz.grade.crud import get_result, get_results, create_result, update_result, delete_result
from app.quiz.grade.models import Result, ResultCreate, ResultRead, ResultUpdate
from app.core.utils.logger import logger_config

router = APIRouter()
logger = logger_config(__name__)


@router.get(
    "",
    response_model=Result,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": Result}},
)
async def health(db: Annotated[AsyncSession, Depends(get_session)]):
    return await get_result(db=db)


@router.post(
    "",
    response_model=Result,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"model": Result}},
)
async def create_new_result(result: ResultCreate, db: Annotated[AsyncSession, Depends(get_session)]):
    return await create_result(result=result, db=db)


@router.get(
    "/all",
    response_model=list[Result],
    status_code=status.HTTP_200_OK,
    responses={200: {"model": list[Result]}},
)
async def get_all_results(db: Annotated[AsyncSession, Depends(get_session)], skip: int = 0, limit: int = 10):
    return await get_results(db=db, skip=skip, limit=limit)


@router.put(
    "",
    response_model=Result,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": Result}},
)
async def update_existing_result(result_id: int, result: ResultUpdate, db: Annotated[AsyncSession, Depends(get_session)]):
    return await update_result(result_id=result_id, result=result, db=db)


@router.delete(
    "",
    response_model=Result,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": Result}},
)
async def delete_existing_result(result_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    return await delete_result(result_id=result_id, db=db)
