"""
Telegram Bot for launching the Tic-Tac-Toe game via Telegram Game API.

Команда /start отправляет пользователю GameMessage,
а Telegram автоматически откроет игру по URL,
указанному в BotFather → /mygames → Edit Game → Game URL.
"""

import logging
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Game,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# ⚠️ ДОЛЖНО СОВПАДАТЬ с GameShortName в BotFather → /mygames
GAME_SHORT_NAME = "tictactoe"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start.
    Отправляет Game message с кнопкой "Играть".
    После нажатия Telegram сам откроет игру по URL в BotFather.
    """
    chat_id = update.effective_chat.id
    logger.info("Sending game to user %s", chat_id)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="▶️ Играть",
                    callback_game={}  # важно: включает Game API
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
    Этот handler вызывается при нажатии кнопки 'Играть'.
    Telegram автоматически откроет Game URL.
    """
    query = update.callback_query
    logger.info("User pressed PLAY, answering callback...")
    await query.answer()


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

    # Основные команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", start))

    # Обработка callback_game
    application.add_handler(CallbackQueryHandler(handle_callback))

    return application


async def run_bot():
    """
    Запуск Telegram-бота.
    Вызывается из main.py.
    """
    app = create_bot_app()

    await app.initialize()
    await app.start()

    # Polling — лучше для Game API
    await app.updater.start_polling()
    logger.info("Telegram bot started.")
