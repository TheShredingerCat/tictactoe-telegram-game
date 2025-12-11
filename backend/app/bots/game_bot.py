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

# Short name должен совпадать с BotFather
GAME_SHORT_NAME = "xo_tictactoy"

# Здесь храним chat_id для каждого user_id
ACTIVE_CHAT_IDS = {}   # user_id → chat_id


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Отправляет кнопку игры пользователю.
    """
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    ACTIVE_CHAT_IDS[user_id] = chat_id
    logger.info(f"[START] Saved chat_id={chat_id} for user_id={user_id}")

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "▶️ Играть",
                callback_game={},       # запускает HTML5 Game
                callback_data="play"    # обязательно, иначе handler не сработает
            )
        ]
    ])

    await context.bot.send_game(
        chat_id=chat_id,
        game_short_name=GAME_SHORT_NAME,
        reply_markup=keyboard,
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Срабатывает при нажатии "Играть".
    Telegram требует вернуть URL игры через answer()
    """
    query: CallbackQuery = update.callback_query
    user_id = query.from_user.id
    chat_id = query.message.chat.id

    ACTIVE_CHAT_IDS[user_id] = chat_id
    logger.info(f"[CALLBACK] PLAY pressed. Saved chat_id={chat_id} for user_id={user_id}")

    # ОБЯЗАТЕЛЬНО — URL HTML5 игры
    await query.answer(url=settings.GAME_URL)


# ---------------------------------------------------------
# Для backend — получить chat_id по user_id
# ---------------------------------------------------------
def get_chat_id(user_id: int):
    return ACTIVE_CHAT_IDS.get(user_id)


# ---------------------------------------------------------
# Запуск Telegram-бота
# ---------------------------------------------------------
def run_bot():
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

    app.run_polling()
