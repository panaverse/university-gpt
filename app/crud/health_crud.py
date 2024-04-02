from sqlmodel import text

from app.core.db import AsyncSession
from app.core.config import logger_config
from app.core import settings

from app.models.health_model import Health, Stats, Status

logger = logger_config(__name__)


async def get_health(db: AsyncSession) -> Health:
    db_status = await health_db(db=db)
    logger.info("%s.get_health.db_status: %s", __name__, db_status)
    return Health(app_status=Status.OK, db_status=db_status, environment=settings.ENV)


async def get_stats(db: AsyncSession) -> Stats:
    stats = Stats(
        university=await count_from_db("university", db),
        program=await count_from_db("program", db),
        course=await count_from_db("course", db),
        topics=await count_from_db("topic", db),
        questions=await count_from_db("questionbank", db),
        quizzes=await count_from_db("quiz", db),
        quiz_settings=await count_from_db("quizsetting", db),
    )
    logger.info("%sget_stats: %s", __name__, stats)
    return stats


async def count_from_db(table: str, db: AsyncSession):
    t = text(f"SELECT COUNT(id) FROM {table};")
    results = await db.execute(t)
    if results is None:
        return 0
    objs = results.scalars().one_or_none()
    return objs if isinstance(objs, int) else objs[0] if objs else 0


async def health_db(db: AsyncSession) -> Status:
    try:
        await db.execute(text("SELECT COUNT(id) FROM topic"))
        return Status.OK
    except Exception as e:
        logger.exception(e)

    return Status.NOT_OK
