import { layout } from "./layout";

const winCodeEl = document.getElementById("win-code") as HTMLElement;
const btnWinAgain = document.getElementById("btn-win-again") as HTMLButtonElement;

export const winScreen = {
  show(code: string) {
    winCodeEl.textContent = code;
    layout.showWinScreen();
  },
};

// Кнопка "Play again"
btnWinAgain.addEventListener("click", () => {
  layout.showGameScreen();
});
