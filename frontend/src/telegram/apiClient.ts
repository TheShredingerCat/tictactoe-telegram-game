import { telegramContext } from "./telegramInit";
import { GameOutcome, PromoResponse } from "../core/types";

/**
 * Базовый URL API.
 * В продакшене заменяется nginx'ом или окружением.
 */
const API_BASE = (window as any).API_BASE ?? "http://localhost:8000";

/**
 * Отправка результата игры на backend.
 *
 * outcome: "win" | "lose"
 * Возвращает промокод или null.
 */
export async function sendGameResult(
  outcome: GameOutcome
): Promise<string | null> {
  try {
    const payload = {
      outcome,
      telegramUserId: telegramContext.userId ?? 0, // backend обработает null как 0
    };

    const response = await fetch(`${API_BASE}/api/game/result`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      console.error("[apiClient] Backend returned error", response.status);
      return null;
    }

    const data = (await response.json()) as PromoResponse;

    if (data.promoCode) {
      return data.promoCode;
    }

    return null;
  } catch (err) {
    console.error("[apiClient] Failed to send game result", err);
    return null;
  }
}
