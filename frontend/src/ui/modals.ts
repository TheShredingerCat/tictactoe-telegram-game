/**
 * Управление модальным окном победы (promo-modal)
 */

import { layout } from "./layout";

const promoModalEl = document.getElementById("promo-modal") as HTMLElement;
const promoCodeEl = document.getElementById("promo-code") as HTMLElement;
const promoPlayAgainBtn = document.getElementById("promo-play-again") as HTMLButtonElement;

export const winScreen = {
  show(code: string) {
    promoCodeEl.textContent = code;
    promoModalEl.classList.remove("promo-modal--hidden");
  },
  hide() {
    promoModalEl.classList.add("promo-modal--hidden");
  }
};

// Кнопка "Play Again" в модалке
promoPlayAgainBtn.addEventListener("click", () => {
  winScreen.hide();
  layout.showGameScreen();
});
