const screenGame = document.getElementById("screen-game") as HTMLElement;
const screenLose = document.getElementById("screen-lose") as HTMLElement;
const screenWin = document.getElementById("screen-win") as HTMLElement;

const statusTextEl = document.getElementById("status-text") as HTMLElement;

export const layout = {
  showGameScreen() {
    screenGame.classList.remove("screen--hidden");
    screenLose.classList.add("screen--hidden");
    screenWin.classList.add("screen--hidden");

    screenGame.classList.add("screen--active");
    screenLose.classList.remove("screen--active");
    screenWin.classList.remove("screen--active");
  },

  showLoseScreen() {
    screenGame.classList.add("screen--hidden");
    screenLose.classList.remove("screen--hidden");
    screenWin.classList.add("screen--hidden");

    screenGame.classList.remove("screen--active");
    screenLose.classList.add("screen--active");
    screenWin.classList.remove("screen--active");
  },

  showWinScreen() {
    screenGame.classList.add("screen--hidden");
    screenLose.classList.add("screen--hidden");
    screenWin.classList.remove("screen--hidden");

    screenGame.classList.remove("screen--active");
    screenLose.classList.remove("screen--active");
    screenWin.classList.add("screen--active");
  },

  setStatus(text: string) {
    statusTextEl.textContent = text;
  },
};
