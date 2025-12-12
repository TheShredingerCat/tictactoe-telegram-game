/**
 * Telegram Game Platform init handler.
 */

export const telegramContext = {
  chat_id: null as number | null,
};

const params = new URLSearchParams(window.location.search);

const chatId =
  params.get("chat_id") ||
  params.get("chatId") ||
  params.get("tgChatId") ||
  null;

if (chatId) {
  telegramContext.chat_id = Number(chatId);
  console.log("[telegramInit] chat_id detected:", telegramContext.chat_id);
} else {
  console.warn("[telegramInit] No chat_id in URL");
}