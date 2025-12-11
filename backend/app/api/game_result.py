from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.services.promo_service import PromoService
from app.services.telegram_service import TelegramService
from app.services.security_service import SecurityService
from app.config import get_settings

# Важно — импортируем chat_id, который бот сохраняет при /start
from app.bots.game_bot import get_chat_id


router = APIRouter()

promo_service = PromoService()
telegram_service = TelegramService()
security_service = SecurityService()
settings = get_settings()


# --------------------------------------------------------
# Pydantic схемы
# --------------------------------------------------------

class GameResultRequest(BaseModel):
    outcome: str            # "win" | "lose"
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


# --------------------------------------------------------
# Endpoint
# --------------------------------------------------------

@router.post("/game/result", response_model=GameResultResponse)
async def game_result(
    payload: GameResultRequest,
    db: Session = Depends(get_session),
):
    """
    При победе:
        1) создаём промокод
        2) отправляем сообщение "Победа! Промокод: XXX"
        3) возвращаем промокод фронту

    При проигрыше:
        1) отправляем сообщение "Проигрыш"
        2) promoCode = None
    """

    # ----------------------------------------------------
    # 1. Определяем Telegram user_id (а значит, и chat_id)
    # ----------------------------------------------------
    user_id = None

    if payload.initData:
        try:
            user_id = security_service.validate_init_data(payload.initData)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid Telegram initData signature"
            )

    if user_id is None:
        user_id = payload.telegramUserId or 0

    # ----------------------------------------------------
    # 2. Получаем chat_id, сохранённый ботом при /start
    # ----------------------------------------------------
    chat_id = get_chat_id(user_id)

    if not chat_id:
        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot determine chat_id for user. "
                "User must press /start in the Telegram bot first."
            )
        )

    # ----------------------------------------------------
    # 3. Ветка победы
    # ----------------------------------------------------
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

    # ----------------------------------------------------
    # 4. Ветка проигрыша
    # ----------------------------------------------------
    await telegram_service.send_lose(chat_id=chat_id)

    return GameResultResponse(
        status="ok",
        promoCode=None
    )
