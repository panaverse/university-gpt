from fastapi import Depends
from typing import Annotated
from app.core.db import AsyncSession, get_async_session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
