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

function detectUserId(): number | null {
  try {
    // Вариант 1: Telegram WebApp API
    if (window.Telegram?.WebApp?.initDataUnsafe?.user) {
      const user = window.Telegram.WebApp.initDataUnsafe.user;
      if (user?.id) return user.id;
    }

    // Вариант 2: Telegram GameProxy API (games.js)
    if (window.TelegramGameProxy?.initParams?.user) {
      const user = window.TelegramGameProxy.initParams.user;
      if (user?.id) return user.id;
    }
  } catch {
    // Если браузер или доступ не из Telegram — просто возвращаем null
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
