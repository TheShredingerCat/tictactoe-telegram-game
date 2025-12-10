/**
 * Управление UI-экранами приложения.
 */

const screenGame = document.getElementById("screen-game") as HTMLElement;
const screenLose = document.getElementById("screen-lose") as HTMLElement;
const statusTextEl = document.getElementById("status-text") as HTMLElement;

export const layout = {
  /**
   * Показывает основной игровой экран.
   */
  showGameScreen() {
    screenGame.classList.remove("screen--hidden");
    screenGame.classList.add("screen--active");

    screenLose.classList.add("screen--hidden");
    screenLose.classList.remove("screen--active");
  },

  /**
   * Показывает экран проигрыша.
   */
  showLoseScreen() {
    screenGame.classList.add("screen--hidden");
    screenGame.classList.remove("screen--active");

    screenLose.classList.remove("screen--hidden");
    screenLose.classList.add("screen--active");
  },

  /**
   * Обновляет текст статуса внизу экрана.
   */
  setStatus(text: string) {
    statusTextEl.textContent = text;
  },
};
