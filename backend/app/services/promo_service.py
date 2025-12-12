import random
from sqlalchemy.orm import Session
from app.bots.game_bot import get_chat_id

from app.models.promo_code import PromoCode


class PromoService:
    """
    Сервис по работе с промокодами:
    - генерация уникального кода
    - сохранение
    - получение данных
    """

    CODE_LENGTH = 5
    MAX_ATTEMPTS = 20  # защита от бесконечного цикла

    @staticmethod
    def _generate_code() -> str:
        """
        Генерирует 5-значный код.
        """
        num = random.randint(0, 10**PromoService.CODE_LENGTH - 1)
        return str(num).zfill(PromoService.CODE_LENGTH)

    def create_promo_code(self, db: Session, chat_id: int) -> PromoCode:
        """
        Генерирует уникальный промокод и сохраняет его в БД.
        """

        for _ in range(self.MAX_ATTEMPTS):
            code = self._generate_code()

            exists = db.query(PromoCode).filter(PromoCode.code == code).first()
            if exists:
                continue

            promo = PromoCode(code=code, chat_id=chat_id)

            db.add(promo)
            db.commit()
            db.refresh(promo)

            return promo

        # Если слишком много коллизий
        raise RuntimeError("Не удалось сгенерировать уникальный промокод")

