from fastapi import Depends
from sqlmodel import Session, text

from api.config import settings
from api.core.database import get_session
from api.quiz.health.models import Health, Stats, Status
from api.core.utils.logger import logger_config

logger = logger_config(__name__)


def get_health(db: Session) -> Health:
    db_status = health_db(db=db)
    logger.info("%s.get_health.db_status: %s", __name__, db_status)
    return Health(app_status=Status.OK, db_status=db_status, environment=settings.ENV)


def get_stats(db: Session) -> Stats:
    stats = Stats(topics=count_from_db("topic", db), questions=count_from_db("questionbank", db))
    logger.info("%sget_stats: %s", __name__, stats)
    return stats


def count_from_db(table: str, db: Session = Depends(get_session)):
    teams = db.exec(text(f"SELECT COUNT(id) FROM {table};")).one_or_none()
    return teams[0] if teams else 0


def health_db(db: Session = Depends(get_session)) -> Status:
    try:
        db.exec(text(f"SELECT COUNT(id) FROM topic;")).one_or_none()
        return Status.OK
    except Exception as e:
        logger.exception(e)

    return Status.KO
