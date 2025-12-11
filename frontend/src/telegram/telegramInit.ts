/**
 * Telegram Game Platform init handler.
 *
 * Задача:
 *  - вытащить user_id из URL, который Telegram передаёт игре
 *  - сохранить в telegramContext
 */

export const telegramContext = {
  userId: null as number | null,
};

// Telegram Games передают параметры через URL вида:
// https://habitbattle.ru/?user_id=337902079&game=xo
// или иногда ?tgUserId=

const params = new URLSearchParams(window.location.search);

const tgUserId =
  params.get("user_id") ||
  params.get("tgUserId") ||
  params.get("userid") ||
  null;

if (tgUserId) {
  telegramContext.userId = Number(tgUserId);
  console.log("[telegramInit] Telegram userId detected:", telegramContext.userId);
} else {
  console.warn("[telegramInit] No Telegram userId found in URL");
}
