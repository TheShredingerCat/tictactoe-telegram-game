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


# --------------------------
# Pydantic модели
# --------------------------

class GameResultRequest(BaseModel):
    outcome: str
    chatId: int | None = None   # <--- теперь принимаем chat_id напрямую

    @field_validator("outcome")
    def validate_outcome(cls, value: str):
        if value not in {"win", "lose"}:
            raise ValueError("outcome must be 'win' or 'lose'")
        return value


class GameResultResponse(BaseModel):
    status: str
    promoCode: str | None = None


# --------------------------
# Endpoint
# --------------------------

@router.post("/game/result", response_model=GameResultResponse)
async def game_result(
    payload: GameResultRequest,
    db: Session = Depends(get_session),
):
    """
    Результат игры. Работаем ТОЛЬКО через chat_id.
    """

    # 1. Проверяем chat_id
    chat_id = payload.chatId

    if not chat_id:
        raise HTTPException(400, "chatId is required")

    # 2. Победа
    if payload.outcome == "win":
        promo = promo_service.create_promo_code(
            db=db,
            chat_id=chat_id
        )

        await telegram_service.send_win(
            chat_id=chat_id,
            promo_code=promo.code
        )

        return GameResultResponse(
            status="ok",
            promoCode=promo.code
        )

    # 3. Поражение
    await telegram_service.send_lose(chat_id=chat_id)

    return GameResultResponse(
        status="ok",
        promoCode=None
    )
