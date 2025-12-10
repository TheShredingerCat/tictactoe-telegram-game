"""
Telegram Bot for launching the Tic-Tac-Toe game via Telegram Game API.

Команда /start отправляет пользователю GameMessage, открывающий игру.
"""

import logging
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    Game,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

# Название игры в Telegram (GameShortName)
GAME_SHORT_NAME = "tictactoe"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start.
    Отправляет Game message.
    """

    chat_id = update.effective_chat.id

    logger.info("Sending game to user %s", chat_id)

    # Inline-кнопка для запуска игры
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="▶️ Играть",
                    callback_game={},   # важно: пустой объект включает Game API
                )
            ]
        ]
    )

    await context.bot.send_game(
        chat_id=chat_id,
        game_short_name=GAME_SHORT_NAME,
        reply_markup=keyboard,
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик callback нажатия кнопки "Играть".
    Telegram автоматически откроет URL игры, который
    ты укажешь в BotFather → Edit Game → URL.
    """

    query = update.callback_query
    await query.answer()  # обязательный ответ

    # Ничего вручную не отправляем — Telegram сам откроет игру по URL
    # согласно настройкам в BotFather.


def create_bot_app() -> Application:
    """
    Создаёт и конфигурирует Telegram-бот приложение.
    """

    application = (
        Application.builder()
        .token(settings.bot_token)
        .concurrent_updates(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", start))  # alias
    application.add_handler(
        # Game callback handler
        # кнопка "callback_game" вызывает его
        CommandHandler("callback", start)
    )

    # Handler для нажатия кнопки запуск игры
    application.add_handler(
        # Это Game Callback, он вызывается автоматически Telegram
        # при нажатии кнопки, содержащей callback_game={}
        CommandHandler("game_callback", start)
    )

    return application


async def run_bot():
    """
    Запуск бота.
    Вызывается из main.py.
    """
    app = create_bot_app()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    logger.info("Telegram bot started.")
