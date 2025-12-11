from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.db.base import Base


class PromoCode(Base):
    """
    ORM-модель промокода.
    """

    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(16), unique=True, nullable=False)

    # Telegram chat id (бывший user_id)
    chat_id = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    used = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<PromoCode id={self.id} code={self.code} user_id={self.user_id}>"
