/**
 * Минимальная инициализация Telegram окружения.
 * Теперь userId нам НЕ нужен, так как chat_id используется через backend.
 */

export interface TelegramContext {
  isTelegram: boolean;
}

function detectIsTelegram(): boolean {
  try {
    if (window.Telegram?.WebApp) return true;
    if (window.TelegramGameProxy) return true;
  } catch {
    return false;
  }
  return false;
}

export const telegramContext: TelegramContext = {
  isTelegram: detectIsTelegram(),
};

console.log("[telegramInit] Telegram environment detected:", telegramContext);
