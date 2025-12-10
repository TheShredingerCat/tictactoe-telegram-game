import logging
from typing import Optional

from telegram import Bot
from telegram.constants import ParseMode

from app.config import get_settings

logger = logging.getLogger(__name__)


class TelegramService:
    """
    Сервис отправки сообщений пользователю в Telegram.
    Использует python-telegram-bot 21.x (асинхронный).
    """

    def __init__(self, token: Optional[str] = None):
        settings = get_settings()
        self.bot = Bot(token or settings.bot_token)

    async def send_win(self, chat_id: int, promo_code: str) -> None:
        """
        Сообщение при победе игрока.
        """
        text = f"Победа! Промокод выдан: {promo_code}"

        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:  # noqa: BLE001
            logger.exception(
                "Failed to send win message to user %s: %s", chat_id, e
            )

    async def send_lose(self, chat_id: int) -> None:
        """
        Сообщение при проигрыше.
        """
        text = "Проигрыш"

        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:  # noqa: BLE001
            logger.exception(
                "Failed to send lose message to user %s: %s", chat_id, e
            )
