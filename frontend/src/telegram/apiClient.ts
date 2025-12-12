import { telegramContext } from "./telegramInit";
import { GameOutcome, PromoResponse } from "../core/types";

const API_BASE = (window as any).API_BASE ?? "https://habitbattle.ru";

export async function sendGameResult(
  outcome: GameOutcome
): Promise<string | null> {
  try {
    const payload = {
      outcome,
      chat_id: telegramContext.chatId,  // ВАЖНО
    };

    console.log("[apiClient] Sending payload:", payload);

    const response = await fetch(`${API_BASE}/api/game/result`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      console.error(
        "[apiClient] Backend returned error",
        response.status,
        await response.text()
      );
      return null;
    }

    const data: PromoResponse = await response.json();
    console.log("[apiClient] Promo response:", data);

    return data.promoCode ?? null;
  } catch (err) {
    console.error("[apiClient] Failed to send game result", err);
    return null;
  }
}
