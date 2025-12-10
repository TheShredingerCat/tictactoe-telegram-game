from functools import lru_cache
from pydantic import BaseModel, Field
import os


class Settings(BaseModel):
    """
    Глобальная конфигурация backend приложения.
    Загружается из переменных окружения, но имеет безопасные дефолты.
    """

    bot_token: str = Field(default="YOUR_BOT_TOKEN", description="Token Telegram Bot API")
    game_url: str = Field(default="https://example.com", description="Public URL игры")
    database_url: str = Field(
        default="sqlite:///./promo.db",
        description="URL базы данных (SQLite для тестового задания)",
    )

    cors_origins: list[str] = Field(
        default=["*"],
        description="Разрешённые источники для CORS (в бою лучше ограничить)"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Кэшированная загрузка настроек.

    Использование:
        from app.config import get_settings
        settings = get_settings()
    """
    return Settings(
        bot_token=os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN"),
        game_url=os.getenv("GAME_URL", "https://example.com"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./promo.db"),
        cors_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    )
