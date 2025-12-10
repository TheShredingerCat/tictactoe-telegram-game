"""
Базовый декларативный класс для всех моделей SQLAlchemy.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Общий Declarative Base.

    Все модели должны наследоваться от Base:
        class PromoCode(Base):
            __tablename__ = "promo_codes"
            ...
    """
    pass
