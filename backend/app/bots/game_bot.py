"""
Telegram Bot for launching the Tic-Tac-Toe game via Telegram Game API.

При нажатии на кнопку "Играть":
1) сохраняем chat_id пользователя
2) Telegram автоматически открывает Game URL (из BotFather)
3) backend при победе/проигрыше отправляет сообщение в этот chat_id
"""

import logging
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
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

# ---------------------------------------------------------
# ГЛОБАЛЬНАЯ ПЕРЕМЕННАЯ — здесь будет chat_id текущего игрока
# ---------------------------------------------------------
active_chat_id: int | None = None

# ⚠️ ДОЛЖНО СОВПАДАТЬ со short_name в BotFather → /mygames
GAME_SHORT_NAME = "xo_tictactoy"


# ---------------------------------------------------------
# Обработчик /start
# ---------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Отправляет игровое сообщение. Telegram сам открывает игру по URL.
    """
    chat_id = update.effective_chat.id
    logger.info("Sending game to user %s", chat_id)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="▶️ Играть",
                callback_game={}     # важно! включает GameMode
            )
        ]
    ])

    await context.bot.send_game(
        chat_id=chat_id,
        game_short_name=GAME_SHORT_NAME,
        reply_markup=keyboard,
    )


# ---------------------------------------------------------
# Обработчик callback от кнопки "Играть"
# ---------------------------------------------------------
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Когда пользователь нажимает кнопку "Играть":
    - сохраняем chat_id
    - Telegram открывает Game URL
    """
    global active_chat_id

    query = update.callback_query
    chat_id = query.message.chat_id
    active_chat_id = chat_id   # <-- ВАЖНО!

    logger.info("User pressed PLAY. Saved active_chat_id: %s", active_chat_id)

    # Ответ на callback обязателен
    await query.answer(
        url="https://habitbattle.ru"   # ваш URL игры
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

    # команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", start))

    # callback_game
    app.add_handler(CallbackQueryHandler(handle_callback))

    return app


# ---------------------------------------------------------
# Запуск бота (вызывается в main.py)
# ---------------------------------------------------------
async def run_bot():
    app = create_bot_app()

    await app.initialize()
    await app.start()

    # Polling нужен именно для Game API
    await app.updater.start_polling()
    logger.info("Telegram game bot started.")
