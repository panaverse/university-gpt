from sqlmodel import text, Session

from app import settings
from app.core.config import logger_config
from app.models.health_models import Health, Stats, Status

logger = logger_config(__name__)


def get_health(db: Session) -> Health:
    db_status = health_db(db=db)
    logger.info("%s.get_health.db_status: %s", __name__, db_status)
    return Health(app_status=Status.OK, db_status=db_status, environment=settings.ENV)


def get_stats(db: Session) -> Stats:
    stats = Stats(
        topic=count_from_db("topic", db),
        content=count_from_db("content", db),
        questionbank=count_from_db("questionbank", db),
        mcqoption=count_from_db("mcqoption", db),
    )
    logger.info("%sget_stats: %s", __name__, stats)
    return stats


def count_from_db(table: str, db: Session):
    t = text(f"SELECT COUNT(id) FROM {table};")
    results = db.exec(t)
    if results is None:
        return 0
    objs = results.scalars().one_or_none()
    return objs if isinstance(objs, int) else objs[0] if objs else 0


def health_db(db: Session) -> Status:
    try:
        db.exec(text("SELECT COUNT(id) FROM topic"))
        return Status.OK
    except Exception as e:
        logger.exception(e)

    return Status.NOT_OK
