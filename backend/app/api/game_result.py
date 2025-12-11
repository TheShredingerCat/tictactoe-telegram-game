from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.services.promo_service import PromoService
from app.services.telegram_service import TelegramService
from app.services.security_service import SecurityService
from app.config import get_settings


router = APIRouter()

promo_service = PromoService()
telegram_service = TelegramService()
security_service = SecurityService()
settings = get_settings()


# -----------------------------
# Pydantic схемы
# -----------------------------

class GameResultRequest(BaseModel):
    outcome: str  # "win" | "lose"
    telegramUserId: int | None = None
    initData: str | None = None

    @field_validator("outcome")
    def outcome_validator(cls, value: str):
        if value not in {"win", "lose"}:
            raise ValueError("outcome must be 'win' or 'lose'")
        return value


class GameResultResponse(BaseModel):
    status: str
    promoCode: str | None = None


# -----------------------------
# Endpoint
# -----------------------------

@router.post("/game/result", response_model=GameResultResponse)
async def game_result(
    payload: GameResultRequest,
    db: Session = Depends(get_session),
):
    """
    При победе:
        1) создаёт промокод (chat_id = user_id = id Telegram-пользователя)
        2) отправляет сообщение "Победа! Промокод: XXX"
        3) возвращает промокод на фронт

    При поражении:
        1) отправляет сообщение "Проигрыш"
        2) promoCode = None
    """

    # ----------------------------------------
    # 1. Определяем Telegram user_id (равен chat_id)
    # ----------------------------------------
    chat_id = None

    # 1) initData через Telegram Game API
    if payload.initData:
        try:
            chat_id = security_service.validate_init_data(payload.initData)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid Telegram initData signature"
            )

    # 2) fallback — если игра передаёт лишь telegramUserId
    if chat_id is None:
        chat_id = payload.telegramUserId or 0

    # ----------------------------------------
    # 2. Ветка победы
    # ----------------------------------------
    if payload.outcome == "win":
        promo = promo_service.create_promo_code(
            db=db,
            chat_id=chat_id,   # FIX HERE
        )

        await telegram_service.send_win(
            chat_id=chat_id,
            promo_code=promo.code
        )

        return GameResultResponse(
            status="ok",
            promoCode=promo.code
        )

    # ----------------------------------------
    # 3. Ветка проигрыша
    # ----------------------------------------
    await telegram_service.send_lose(chat_id=chat_id)

    return GameResultResponse(
        status="ok",
        promoCode=None
    )
