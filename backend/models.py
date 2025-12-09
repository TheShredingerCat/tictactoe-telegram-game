from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(Integer, unique=True, index=True, nullable=False)

    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    draws = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_game_at = Column(DateTime, default=datetime.utcnow)

    promo_codes = relationship("PromoCode", back_populates="player")

    def achievement_title(self) -> str:
        """Простая система ачивок по количеству побед."""
        w = self.wins
        if w >= 20:
            return "Легенда"
        if w >= 10:
            return "Профи"
        if w >= 5:
            return "Тактик"
        if w >= 1:
            return "Новичок"
        return "Гость"


class PromoCode(Base):
    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(16), unique=True, index=True, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    player = relationship("Player", back_populates="promo_codes")
