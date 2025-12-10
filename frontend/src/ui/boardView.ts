import { Board } from "../core/types";

/**
 * Контроллер отображения игрового поля и кликов игрока.
 */

const boardEl = document.getElementById("board") as HTMLElement;
const cellElements: HTMLButtonElement[] = Array.from(
  boardEl.querySelectorAll(".cell")
) as HTMLButtonElement[];

const cellInners: HTMLElement[] = [];

/**
 * Инициализация DOM-структуры клеток
 * В каждую клетку вставляется <div class="cell-inner">,
 * чтобы можно было легко менять X/O.
 */
cellElements.forEach((cell) => {
  const inner = document.createElement("div");
  inner.className = "cell-inner";
  cell.appendChild(inner);
  cellInners.push(inner);
});

/**
 * Коллбэк, вызываемый при клике на клетку
 */
let onCellClickHandler: (index: number) => void = () => {};

/**
 * Публичный интерфейс
 */
export const boardView = {
  /**
   * Устанавливает обработчик кликов по клетке.
   */
  onCellClick(handler: (index: number) => void) {
    onCellClickHandler = handler;
  },

  /**
   * Делает все клетки активными или неактивными.
   */
  setEnabled(enabled: boolean) {
    cellElements.forEach((cell) => {
      cell.disabled = !enabled;
    });
  },

  /**
   * Подписывается на клики по реальным DOM-кнопкам.
   */
  initClickListeners() {
    cellElements.forEach((cell) => {
      cell.addEventListener("click", () => {
        const index = Number(cell.dataset.index);
        onCellClickHandler(index);
      });
    });
  },

  /**
   * Перерисовывает X/O на поле.
   */
  render(board: Board) {
    board.forEach((value, idx) => {
      const inner = cellInners[idx];
      inner.classList.remove("cell-inner--x", "cell-inner--o");

      if (value === "X") {
        inner.classList.add("cell-inner--x");
      } else if (value === "O") {
        inner.classList.add("cell-inner--o");
      }
    });
  },
};
