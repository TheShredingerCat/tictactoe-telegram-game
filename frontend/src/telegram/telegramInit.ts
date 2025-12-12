/**
 * Telegram Game Init — читаем chat_id из URL
 */

export const telegramContext = {
  chatId: null as number | null,
};

const params = new URLSearchParams(window.location.search);

const chatId = params.get("chat_id");

if (chatId) {
  telegramContext.chatId = Number(chatId);
  console.log("[telegramInit] chat_id detected:", telegramContext.chatId);
} else {
  console.warn("[telegramInit] No chat_id in URL");
}
