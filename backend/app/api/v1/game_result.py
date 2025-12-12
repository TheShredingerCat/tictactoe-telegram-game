from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.services.promo_service import PromoService
from app.services.telegram_service import TelegramService
from app.config import get_settings

router = APIRouter()

promo_service = PromoService()
telegram_service = TelegramService()
settings = get_settings()


class GameResultRequest(BaseModel):
    outcome: str
    chat_id: int   # ТОЛЬКО chat_id

    @field_validator("outcome")
    def validate_outcome(cls, v):
        if v not in ("win", "lose"):
            raise ValueError("outcome must be 'win' or 'lose'")
        return v


class GameResultResponse(BaseModel):
    status: str
    promoCode: str | None = None


@router.post("/game/result", response_model=GameResultResponse)
async def game_result(payload: GameResultRequest, db: Session = Depends(get_session)):
    """
    Обрабатываем победу или проигрыш, используя только chat_id.
    """

    chat_id = payload.chat_id
    if not chat_id:
        raise HTTPException(400, "chat_id is required")

    # ---------- Победа ----------
    if payload.outcome == "win":
        promo = promo_service.create_promo_code(db=db, chat_id=chat_id)

        await telegram_service.send_win(chat_id=chat_id, promo_code=promo.code)

        return GameResultResponse(
            status="ok",
            promoCode=promo.code
        )

    # ---------- Проигрыш ----------
    await telegram_service.send_lose(chat_id=chat_id)

    return GameResultResponse(
        status="ok",
        promoCode=None
    )
