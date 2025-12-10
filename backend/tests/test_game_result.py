import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_session
from app.api.v1.game_result import router
from app.services.telegram_service import TelegramService


# -----------------------------
# Переопределяем TelegramService моками
# -----------------------------

class MockTelegramService:
    async def send_win(self, chat_id: int, promo_code: str):
        self.last_win = (chat_id, promo_code)

    async def send_lose(self, chat_id: int):
        self.last_lose = chat_id


# -----------------------------
# Тестовая база данных
# -----------------------------

@pytest.fixture()
def app():
    engine = create_engine("sqlite:///:memory:", future=True)
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        future=True
    )

    # Создаём таблицы
    Base.metadata.create_all(bind=engine)

    # FastAPI
    app = FastAPI()
    app.include_router(router, prefix="/api")

    # Подменяем зависимость get_session
    async def override_get_session():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_session] = override_get_session

    # Подменяем TelegramService в модуле
    mock_service = MockTelegramService()
    TelegramService.send_win = mock_service.send_win
    TelegramService.send_lose = mock_service.send_lose

    return app


# -----------------------------
# Тест win
# -----------------------------

@pytest.mark.asyncio
async def test_game_result_win(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.post(
            "/api/game/result",
            json={"outcome": "win", "telegramUserId": 123},
        )

    assert resp.status_code == 200
    data = resp.json()

    assert data["promoCode"] is not None
    assert len(data["promoCode"]) == 5
    assert data["status"] == "ok"


# -----------------------------
# Тест lose
# -----------------------------

@pytest.mark.asyncio
async def test_game_result_lose(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.post(
            "/api/game/result",
            json={"outcome": "lose", "telegramUserId": 321},
        )

    assert resp.status_code == 200
    data = resp.json()

    assert data["promoCode"] is None
    assert data["status"] == "ok"
