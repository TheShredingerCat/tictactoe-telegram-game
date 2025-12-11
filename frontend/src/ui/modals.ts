import { layout } from "./layout";

const promoModalEl = document.getElementById("promo-modal") as HTMLElement;
const promoCodeEl = document.getElementById("promo-code") as HTMLElement;
const promoPlayAgainBtn = document.getElementById("promo-play-again") as HTMLButtonElement;

export const winModal = {
  show(code: string) {
    promoCodeEl.textContent = code;
    layout.showWinModal();
  },
  hide() {
    layout.hideWinModal();
  }
};

promoPlayAgainBtn.addEventListener("click", () => {
  winModal.hide();
  layout.showGameScreen();
});
