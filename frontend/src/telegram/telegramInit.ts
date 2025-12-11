/**


export interface TelegramContext {
  userId: number | null;
  isTelegram: boolean;
}

function parseUserId(source: string | null | undefined): number | null {
  if (!source) return null;

  const match = source.match(/(?:^|[?&#])(tg_user_id|user_id)=(\d+)/);
  if (!match) return null;

  const parsed = Number(match[2]);
  return Number.isFinite(parsed) ? parsed : null;
}

function detectUserId() {
  try {
    if (window.Telegram?.WebApp?.initDataUnsafe?.user?.id) {
      return window.Telegram.WebApp.initDataUnsafe.user.id;
    }

    if (window.TelegramGameProxy?.initParams?.user?.id) {
      return window.TelegramGameProxy.initParams.user.id;
    }

    // 3) fallback: look for tg_user_id anywhere in the URL (query or hash)
    const direct = parseUserId(window.location.href);
    if (direct !== null) {
      return direct;
    }

    const hashParams = new URLSearchParams(
      window.location.hash?.startsWith("#")
        ? window.location.hash.slice(1)
        : window.location.hash ?? ""
    );
    const searchParams = new URLSearchParams(
      window.location.search?.startsWith("?")
        ? window.location.search.slice(1)
        : window.location.search ?? ""
    );

    const tgShareScoreUrl =
      hashParams.get("tgShareScoreUrl") ?? searchParams.get("tgShareScoreUrl");

    const decodedShare = tgShareScoreUrl
      ? decodeURIComponent(tgShareScoreUrl)
      : null;

    const fromShare = parseUserId(decodedShare);
    if (fromShare !== null) {
      return fromShare;
    }
  } catch (e) {
    console.warn("Telegram detection error", e);
  }

  return null;
}


const userId = detectUserId();

/**

 */
export const telegramContext: TelegramContext = {
  userId,
  isTelegram: userId !== null,
};

console.log("[telegramInit] Context:", telegramContext);
