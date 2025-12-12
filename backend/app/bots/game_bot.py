import logging
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
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

GAME_SHORT_NAME = "xo_tictactoy"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Отправляем кнопку игры. В URL игры передаём chat_id.
    """
    chat_id = update.effective_chat.id

    logger.info(f"[START] chat_id={chat_id}")

    game_url = f"https://habitbattle.ru/?chat_id={chat_id}"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "▶️ Играть",
                callback_game={},  # запускает HTML5 Game
            )
        ]
    ])

    await context.bot.send_game(
        chat_id=chat_id,
        game_short_name=GAME_SHORT_NAME,
        reply_markup=keyboard,
        start_parameter=str(chat_id)
    )



async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Когда пользователь нажимает PLAY — открываем игру со своим chat_id.
    """
    query: CallbackQuery = update.callback_query
    chat_id = query.message.chat.id

    logger.info(f"[CALLBACK] PLAY pressed — chat_id={chat_id}")

    # Передаём chat_id в игру
    await query.answer(url=f"https://habitbattle.ru/?chat_id={chat_id}&v=3")


async def run_bot():
    logger.info("Starting Telegram game bot...")

    app = (
        Application.builder()
        .token(settings.bot_token)
        .concurrent_updates(True)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", start))
    app.add_handler(CallbackQueryHandler(handle_callback))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
