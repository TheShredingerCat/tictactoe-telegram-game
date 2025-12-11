const screenGame = document.getElementById("screen-game") as HTMLElement;
const screenLose = document.getElementById("screen-lose") as HTMLElement;
const promoModalEl = document.getElementById("promo-modal") as HTMLElement;
const statusTextEl = document.getElementById("status-text") as HTMLElement;

export const layout = {
  showGameScreen() {
    screenGame.classList.remove("screen--hidden");
    screenLose.classList.add("screen--hidden");
    promoModalEl.classList.add("promo-modal--hidden");
  },

  showLoseScreen() {
    screenGame.classList.add("screen--hidden");
    screenLose.classList.remove("screen--hidden");
    promoModalEl.classList.add("promo-modal--hidden");
  },

  showWinModal() {
    promoModalEl.classList.remove("promo-modal--hidden");
  },

  hideWinModal() {
    promoModalEl.classList.add("promo-modal--hidden");
  },

  setStatus(text: string) {
    statusTextEl.textContent = text;
  },
};
