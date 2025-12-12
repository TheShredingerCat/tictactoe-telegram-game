/**
 * Telegram Game Platform init handler.
 */

export const telegramContext = {
  chatId: null as number | null,
};

const params = new URLSearchParams(window.location.search);

const id = params.get("chat_id");
if (id) {
  telegramContext.chatId = Number(id);
  console.log("[telegramInit] chat_id detected:", telegramContext.chatId);
} else {
  console.warn("[telegramInit] No chat_id in URL");
}
