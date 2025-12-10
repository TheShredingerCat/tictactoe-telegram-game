import { Board, CellValue, PlayerSymbol, Winner } from "./types";

/**
 * Создаёт пустое поле размером 3x3.
 */
export function createEmptyBoard(): Board {
  return Array(9).fill(null);
}

/**
 * Проверяет, свободна ли клетка.
 */
export function isCellEmpty(board: Board, index: number): boolean {
  return board[index] === null;
}

/**
 * Совершает ход игрока или бота.
 * Возвращает новое состояние поля.
 */
export function makeMove(
  board: Board,
  index: number,
  symbol: PlayerSymbol
): Board {
  if (!isCellEmpty(board, index)) return board;

  const nextBoard = [...board];
  nextBoard[index] = symbol;
  return nextBoard;
}

/**
 * Возвращает список свободных клеток.
 */
export function getAvailableMoves(board: Board): number[] {
  const moves: number[] = [];
  for (let i = 0; i < board.length; i++) {
    if (board[i] === null) moves.push(i);
  }
  return moves;
}

/**
 * Проверяет окончание игры.
 * Возвращает "X", "O", "draw" или null.
 */
export function checkWinner(board: Board): Winner {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],

    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],

    [0, 4, 8],
    [2, 4, 6],
  ];

  for (const [a, b, c] of lines) {
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      return board[a];
    }
  }

  const isDraw = board.every((cell) => cell !== null);
  return isDraw ? "draw" : null;
}
