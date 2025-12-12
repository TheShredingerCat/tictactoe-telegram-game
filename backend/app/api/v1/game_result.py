from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.services.promo_service import PromoService
from app.services.telegram_service import TelegramService
from app.services.security_service import SecurityService
from app.config import get_settings

from app.bots.game_bot import get_chat_id


router = APIRouter()

promo_service = PromoService()
telegram_service = TelegramService()
security_service = SecurityService()
settings = get_settings()


class GameResultRequest(BaseModel):
    outcome: str
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


@router.post("/game/result", response_model=GameResultResponse)
async def game_result(
    payload: GameResultRequest,
    db: Session = Depends(get_session),
):
    """
    Обрабатываем победу/поражение.
    """

    # -------------------------------
    # 1. Определяем user_id
    # -------------------------------
    user_id = None

    if payload.initData not in (None, "", "null"):
        try:
            user_id = security_service.validate_init_data(payload.initData)
        except Exception:
            raise HTTPException(400, "Invalid Telegram initData signature")


    if user_id is None:
        user_id = payload.telegramUserId or 0

    # -------------------------------
    # 2. Получаем chat_id бота
    # -------------------------------
    chat_id = get_chat_id(user_id)

    if not chat_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot determine chat_id — user must press /start in bot"
        )

    # -------------------------------
    # 3. Победа
    # -------------------------------
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

    # -------------------------------
    # 4. Проигрыш
    # -------------------------------
    await telegram_service.send_lose(chat_id=chat_id)

    return GameResultResponse(
        status="ok",
        promoCode=None
    )
