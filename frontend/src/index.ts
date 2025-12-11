import { Board, Winner } from "./core/types";
import { createEmptyBoard, makeMove, checkWinner } from "./core/gameEngine";
import { PLAYER, BOT, chooseBotMove } from "./core/botAI";
import { boardView } from "./ui/boardView";
import { layout } from "./ui/layout";
import { winModal } from "./ui/modals";
import { sendGameResult } from "./telegram/apiClient";

let board: Board = createEmptyBoard();
let isPlayerTurn = true;
let gameOver = false;

function init() {
  boardView.initClickListeners();

  boardView.onCellClick((index) => handlePlayerMove(index));

  document.getElementById("btn-reset")?.addEventListener("click", startNewGame);
  document.getElementById("btn-lose-again")?.addEventListener("click", () => {
    layout.showGameScreen();
    startNewGame();
  });

  startNewGame();
}

init();

function startNewGame() {
  board = createEmptyBoard();
  isPlayerTurn = true;
  gameOver = false;

  layout.setStatus("Ваш ход");
  layout.showGameScreen();
  boardView.setEnabled(true);
  boardView.render(board);
}

function handlePlayerMove(index: number) {
  if (!isPlayerTurn || gameOver) return;
  if (board[index] !== null) return;

  board = makeMove(board, index, PLAYER);
  boardView.render(board);

  const winner = checkWinner(board);
  if (winner) return endGame(winner);

  isPlayerTurn = false;
  layout.setStatus("Компьютер думает…");

  setTimeout(botTurn, 300);
}

function botTurn() {
  if (gameOver) return;

  const move = chooseBotMove(board);
  if (move !== null) {
    board = makeMove(board, move, BOT);
    boardView.render(board);
  }

  const winner = checkWinner(board);
  if (winner) return endGame(winner);

  isPlayerTurn = true;
  layout.setStatus("Ваш ход");
}

async function endGame(winner: Winner) {
  gameOver = true;
  boardView.setEnabled(false);

  if (winner === PLAYER) {
    layout.setStatus("Вы победили!");

    const promo = await sendGameResult("Победа");
    const code = promo ?? "00000";

    winModal.show(code);
    return;
  }

  if (winner === BOT) {
    layout.setStatus("Вы проиграли.");

    await sendGameResult("Проигрыш");
    layout.showLoseScreen();
    return;
  }

  layout.setStatus("Ничья! Нажмите чтобы сыграть снова.");
}
