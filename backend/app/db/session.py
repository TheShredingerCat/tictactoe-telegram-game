"""
Настройка SQLAlchemy Engine и сессий.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import get_settings

settings = get_settings()

# Создаем engine
engine = create_engine(
    settings.database_url,
    echo=False,            # echo=True можно включить для отладки SQL
    future=True
)

# Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
    future=True
)


def get_session() -> Session:
    """
    Dependency для FastAPI.
    Возвращает новую session для каждого запроса.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
