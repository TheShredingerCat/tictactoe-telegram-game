import random
from sqlalchemy.orm import Session

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
        Пример: "02714", "98310"
        """
        num = random.randint(0, 10**PromoService.CODE_LENGTH - 1)
        return str(num).zfill(PromoService.CODE_LENGTH)

    def create_promo_code(self, db: Session, user_id: int) -> PromoCode:
        """
        Генерирует уникальный промокод и сохраняет его в БД.
        """

        for _ in range(self.MAX_ATTEMPTS):
            code = self._generate_code()

            # Проверяем уникальность
            exists = (
                db.query(PromoCode)
                .filter(PromoCode.code == code)
                .first()
            )

            if exists:
                continue

            # Создаём объект
            promo = PromoCode(
                code=code,
                user_id=user_id,
            )

            db.add(promo)
            db.commit()
            db.refresh(promo)

            return promo

        # Если мы тут — что-то совсем странное (очень много коллизий)
        raise RuntimeError("Не удалось сгенерировать уникальный промокод")

