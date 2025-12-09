from datetime import datetime
import random

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import DATABASE_URL
from database import Base, engine, SessionLocal
from models import Player, PromoCode
from telegram_utils import send_message_to_user

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TicTacToe Telegram Game API")

# CORS — чтобы фронт мог стучаться
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можешь сузить до своего домена
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Зависимость для сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class GameResult(BaseModel):
    userId: int
    result: str  # "win" | "lose" | "draw"
    promoCode: str | None = None  # фронт можно не использовать, мы генерим на бэке


# ----- вспомогательные функции -----

def get_or_create_player(db: Session, telegram_user_id: int) -> Player:
    player = db.query(Player).filter_by(telegram_user_id=telegram_user_id).first()
    if not player:
        player = Player(telegram_user_id=telegram_user_id)
        db.add(player)
        db.commit()
        db.refresh(player)
    return player


def generate_unique_promo(db: Session) -> str:
    """Генерим уникальный 5-значный промокод."""
    while True:
        code = str(random.randint(0, 99999)).zfill(5)
        exists = db.query(PromoCode).filter_by(code=code).first()
        if not exists:
            return code


# ----- эндпоинт, который дергает игра -----

@app.post("/api/game-result")
async def api_game_result(data: GameResult, db: Session = Depends(get_db)):
    player = get_or_create_player(db, data.userId)

    player.last_game_at = datetime.utcnow()

    promo_code_value: str | None = None
    achievement: str | None = None

    # обновляем статистику
    if data.result == "win":
        player.wins += 1

        # генерим уникальный промокод и сохраняем
        promo_code_value = generate_unique_promo(db)
        promo = PromoCode(code=promo_code_value, player_id=player.id)
        db.add(promo)

        db.commit()
        db.refresh(player)

        achievement = player.achievement_title()

        # сообщение в Telegram
        text_lines = [
            "🎉 <b>Победа!</b>",
            f"Ваш промокод: <code>{promo_code_value}</code>",
        ]
        if achievement:
            text_lines.append(f"Текущий статус: <b>{achievement}</b>")
        text = "\n".join(text_lines)

        await send_message_to_user(player.telegram_user_id, text)

        return {"status": "ok", "promoCode": promo_code_value, "achievement": achievement}

    elif data.result == "lose":
        player.losses += 1
        db.commit()
        db.refresh(player)

        achievement = player.achievement_title()

        text = "❌ Проигрыш. Попробуйте ещё раз — победа ближе, чем кажется 🙂"
        await send_message_to_user(player.telegram_user_id, text)

        return {"status": "ok", "achievement": achievement}

    elif data.result == "draw":
        player.draws += 1
        db.commit()
        db.refresh(player)
        # по исходному ТЗ при ничьей — без Telegram
        achievement = player.achievement_title()
        return {"status": "ok", "achievement": achievement}

    return {"status": "ignored"}
