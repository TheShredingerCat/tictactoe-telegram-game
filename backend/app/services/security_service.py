"""
Security service — валидация initData Telegram WebApp/Game.
"""

import hmac
import hashlib
import urllib.parse
from typing import Dict, Any, Optional

from app.config import get_settings


class TelegramSecurityException(Exception):
    """Ошибка проверки подписи Telegram initData."""


class SecurityService:
    """
    Проверяет подпись Telegram initData:
    https://core.telegram.org/bots/webapps#initializing-mini-apps
    """

    @staticmethod
    def _parse_init_data(init_data: str) -> Dict[str, Any]:
        """
        Преобразует строку query_string в словарь.
        """
        parsed = dict(urllib.parse.parse_qsl(init_data, keep_blank_values=True))
        return parsed

    @staticmethod
    def _compute_hash(init_dict: Dict[str, Any], bot_token: str) -> str:
        """
        Telegram требует HMAC-SHA256(hash_data, secret_key)

        secret_key = SHA256(bot_token)
        """
        # 1. Получаем secret key
        secret_key = hashlib.sha256(bot_token.encode()).digest()

        # 2. Готовим строку данных (без hash)
        check_data = "\n".join(
            f"{k}={v}"
            for k, v in sorted(init_dict.items())
            if k != "hash"
        )

        h = hmac.new(secret_key, check_data.encode(), hashlib.sha256)
        return h.hexdigest()

    def validate_init_data(self, init_data: str) -> Optional[int]:
        """
        Проверяет подпись initData и возвращает user_id.
        Если initData пустой — считаем, что игра не из Telegram.
        """

        if not init_data:
            return None

        settings = get_settings()
        data_dict = self._parse_init_data(init_data)

        received_hash = data_dict.get("hash")
        if not received_hash:
            raise TelegramSecurityException("Hash not provided in initData")

        computed_hash = self._compute_hash(data_dict, bot_token=settings.bot_token)

        if not hmac.compare_digest(received_hash, computed_hash):
            raise TelegramSecurityException("Invalid initData signature")

        # Telegram передаёт user JSON внутри initData
        # Например: user={"id":12345,"first_name":"..."}
        user_raw = data_dict.get("user")
        if not user_raw:
            return None

        # Превращаем JSON в dict
        import json

        try:
            user = json.loads(user_raw)
            return user.get("id")
        except Exception:
            raise TelegramSecurityException("Invalid 'user' JSON content")
