/**
 * РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ РѕРєСЂСѓР¶РµРЅРёСЏ Telegram.
 *
 * РРіСЂР° РјРѕР¶РµС‚ Р·Р°РїСѓСЃРєР°С‚СЊСЃСЏ РІ РґРІСѓС… СЂРµР¶РёРјР°С…:
 * 1. Р§РµСЂРµР· Telegram WebApp API (new, mobile)
 * 2. Р§РµСЂРµР· Telegram Game API (СЃС‚Р°СЂС‹Р№ GameProxy)
 *
 * РќР°С€Р° Р·Р°РґР°С‡Р° вЂ” Р±РµР·РѕРїР°СЃРЅРѕ РїРѕР»СѓС‡РёС‚СЊ userId.
 */

export interface TelegramContext {
  userId: number | null;
  isTelegram: boolean;
}

function detectUserId() {
  try {
    // 1) WebApp API (РµСЃР»Рё РІРґСЂСѓРі РѕС‚РєСЂРѕРµС‚СЃСЏ РєР°Рє WebApp)
    if (window.Telegram?.WebApp?.initDataUnsafe?.user?.id) {
      return window.Telegram.WebApp.initDataUnsafe.user.id;
    }

    // 2) Game API (С‚РІРѕСЏ СЃРёС‚СѓР°С†РёСЏ)
    if (window.TelegramGameProxy?.initParams?.user?.id) {
      return window.TelegramGameProxy.initParams.user.id;
    }
    // 3) fallback: user id from query parameter (?tg_user_id=123)
    const querySources = [window.location.search, window.location.hash];
    for (const source of querySources) {
      if (!source) continue;

      const withoutPrefix =
        source.startsWith("?") || source.startsWith("#")
          ? source.slice(1)
          : source;

      const queryIndex = withoutPrefix.indexOf("?");
      const query =
        queryIndex >= 0 ? withoutPrefix.slice(queryIndex + 1) : withoutPrefix;
      if (!query) continue;

      const params = new URLSearchParams(query);
      const fromQuery = params.get("tg_user_id") ?? params.get("user_id");
      if (fromQuery) {
        const parsed = Number(fromQuery);
        if (!Number.isNaN(parsed) && Number.isFinite(parsed)) {
          return parsed;
        }
      }
    }

  } catch (e) {
    console.warn("Telegram detection error", e);
  }

  return null;
}


const userId = detectUserId();

/**
 * РљРѕРЅС‚РµРєСЃС‚, РєРѕС‚РѕСЂС‹Р№ РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РІРѕ РІСЃРµС… Telegram API РІС‹Р·РѕРІР°С….
 */
export const telegramContext: TelegramContext = {
  userId,
  isTelegram: userId !== null,
};

console.log("[telegramInit] Context:", telegramContext);
