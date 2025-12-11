/**
 * Инициализация окружения Telegram.
 *
 * Игра может запускаться в двух режимах:
 * 1. Через Telegram WebApp API (new, mobile)
 * 2. Через Telegram Game API (старый GameProxy)
 *
 * Наша задача — безопасно получить userId.
 */

export interface TelegramContext {
  userId: number | null;
  isTelegram: boolean;
}

function detectUserId() {
  try {
    // 1) WebApp API (если вдруг откроется как WebApp)
    if (window.Telegram?.WebApp?.initDataUnsafe?.user?.id) {
      return window.Telegram.WebApp.initDataUnsafe.user.id;
    }

    // 2) Game API (твоя ситуация)
    if (window.TelegramGameProxy?.initParams?.user?.id) {
      return window.TelegramGameProxy.initParams.user.id;
    }
  } catch (e) {
    console.warn("Telegram detection error", e);
  }

  return null;
}


const userId = detectUserId();

/**
 * Контекст, который используется во всех Telegram API вызовах.
 */
export const telegramContext: TelegramContext = {
  userId,
  isTelegram: userId !== null,
};

console.log("[telegramInit] Context:", telegramContext);
