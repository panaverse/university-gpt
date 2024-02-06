from sqlmodel import text

from api.config import settings
from api.core.database import AsyncSession
from api.quiz.health.models import Health, Stats, Status
from api.core.utils.logger import logger_config

logger = logger_config(__name__)


async def get_health(db: AsyncSession) -> Health:
    db_status = await health_db(db=db)
    logger.info("%s.get_health.db_status: %s", __name__, db_status)
    return Health(app_status=Status.OK, db_status=db_status, environment=settings.ENV)


async def get_stats(db: AsyncSession) -> Stats:
    stats = Stats(
        topics=await count_from_db("topic", db), 
        questions=await count_from_db("questionbank", db)
        )
    logger.info("%sget_stats: %s", __name__, stats)
    return stats


async def count_from_db(table: str, db: AsyncSession):
    results = await db.execute(text(f"SELECT COUNT(id) FROM {table};"))
    teams = results.scalars().one_or_none()
    return teams[0] if teams else 0


async def health_db(db: AsyncSession) -> Status:
    try:
        await db.execute(text(f"SELECT COUNT(id) FROM topic;"))
        return Status.OK
    except Exception as e:
        logger.exception(e)

    return Status.KO
