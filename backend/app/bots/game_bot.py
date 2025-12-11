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

# ДОЛЖНО совпадать с short_name в BotFather
GAME_SHORT_NAME = "xo_tictactoy"

# Здесь храним chat_id активного игрока
ACTIVE_CHAT_ID = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ACTIVE_CHAT_ID

    chat_id = update.effective_chat.id
    ACTIVE_CHAT_ID = chat_id  # <- сохраняем chat_id

    logger.info(f"Sending game to user {chat_id}")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ Играть", callback_game={})]
    ])

    await context.bot.send_game(
        chat_id=chat_id,
        game_short_name=GAME_SHORT_NAME,
        reply_markup=keyboard,
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Запоминаем chat_id при нажатии на кнопку Играть
    """
    global ACTIVE_CHAT_ID

    query: CallbackQuery = update.callback_query
    chat_id = query.message.chat.id

    ACTIVE_CHAT_ID = chat_id 
    logger.info(f"User pressed PLAY. Saved ACTIVE_CHAT_ID={ACTIVE_CHAT_ID}")

    await query.answer(
        url="https://habitbattle.ru" 
    )


# ---------------------------------------------------------
# Создание приложения бота
# ---------------------------------------------------------
def create_bot_app() -> Application:
    app = (
        Application.builder()
        .token(settings.bot_token)
        .concurrent_updates(True)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", start))
    app.add_handler(CallbackQueryHandler(handle_callback))

    return app
