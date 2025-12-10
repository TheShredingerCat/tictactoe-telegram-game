"""
Главная точка входа backend сервиса:
- FastAPI приложение
- Telegram Bot (через асинхронный фоновой таск)
- Инициализация БД
"""

import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.session import engine, get_session
from app.db.base import Base

from app.api.v1.game_result import router as game_result_router
from app.bots.game_bot import run_bot


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


# -------------------------------------------------------
# Создание таблиц (для SQLite тестового проекта)
# -------------------------------------------------------

def init_database():
    """
    Создаём таблицы, если их ещё нет.
    В продакшене используется Alembic, но для тестового достаточно Base.metadata.create_all.
    """
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized.")


# -------------------------------------------------------
# FastAPI application
# -------------------------------------------------------

app = FastAPI(title="TicTacToe Telegram Game API")

# CORS (для локальной разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# -------------------------------------------------------
# Роуты API
# -------------------------------------------------------

app.include_router(game_result_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}


# -------------------------------------------------------
# Telegram bot launcher
# -------------------------------------------------------

@app.on_event("startup")
async def on_startup():
    logger.info("Starting backend...")

    # Создаём таблицы
    init_database()

    # Запуск телеграм-бота в фоне
    asyncio.create_task(run_bot())
    logger.info("Telegram bot started in background.")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down backend...")
