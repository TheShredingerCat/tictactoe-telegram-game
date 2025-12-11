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
    Принимает результат игры.
    
    При победе:
        1) создаёт промокод
        2) отправляет сообщение "Победа! Промокод выдан: {код}"
        3) возвращает промокод на фронт

    При проигрыше:
        1) отправляет сообщение "Проигрыш"
        2) promoCode = None
    """

    # -----------------------------
    # Определяем user_id
    # -----------------------------
    user_id = None

    # 1) initData через Telegram WebApp/Game API
    if payload.initData:
        try:
            user_id = security_service.validate_init_data(payload.initData)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid Telegram initData signature"
            )

    # 2) Если initData нет — fallback на telegramUserId
    if user_id is None:
        user_id = payload.telegramUserId or 0

    # -----------------------------
    # Ветка победы
    # -----------------------------
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

    # -----------------------------
    # Ветка проигрыша
    # -----------------------------
    await telegram_service.send_lose(chat_id=user_id)

    return GameResultResponse(
        status="ok",
        promoCode=None
    )
