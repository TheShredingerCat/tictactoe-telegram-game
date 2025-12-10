import { Board, PlayerSymbol } from "./types";
import {
  getAvailableMoves,
  makeMove,
  checkWinner,
} from "./gameEngine";

/**
 * Символы игрока и бота.
 */
export const PLAYER: PlayerSymbol = "X";
export const BOT: PlayerSymbol = "O";

/**
 * Выбирает ход бота.
 * Возвращает индекс клетки или null, если ходов нет.
 */
export function chooseBotMove(board: Board): number | null {
  const available = getAvailableMoves(board);

  if (available.length === 0) return null;

  // 1. Бот может выиграть?
  for (const index of available) {
    const testBoard = makeMove(board, index, BOT);
    if (checkWinner(testBoard) === BOT) {
      return index;
    }
  }

  // 2. Игрок может выиграть — блокируем
  for (const index of available) {
    const testBoard = makeMove(board, index, PLAYER);
    if (checkWinner(testBoard) === PLAYER) {
      return index;
    }
  }

  // 3. Центр
  if (available.includes(4)) return 4;

  // 4. Углы
  const corners = [0, 2, 6, 8];
  const cornerMoves = corners.filter((i) => available.includes(i));
  if (cornerMoves.length > 0) {
    return cornerMoves[Math.floor(Math.random() * cornerMoves.length)];
  }

  // 5. Любая доступная клетка
  return available[Math.floor(Math.random() * available.length)];
}
