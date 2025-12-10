import { Board, Winner } from "./core/types";
import {
  createEmptyBoard,
  makeMove,
  checkWinner,
  getAvailableMoves,
} from "./core/gameEngine";

import { PLAYER, BOT, chooseBotMove } from "./core/botAI";

import { boardView } from "./ui/boardView";
import { layout } from "./ui/layout";
import { promoModal } from "./ui/modals";
import { sendGameResult } from "./telegram/apiClient";

// ---------------------------
// GLOBAL STATE
// ---------------------------

let board: Board = createEmptyBoard();
let isPlayerTurn = true;
let gameOver = false;

// ---------------------------
// INITIALIZATION
// ---------------------------

function init() {
  boardView.initClickListeners();

  boardView.onCellClick((index) => {
    handlePlayerMove(index);
  });

  promoModal.setHandlers({
    onPlayAgain() {
      startNewGame();
    },
  });

  const loseBtn = document.getElementById("btn-lose-again");
  loseBtn?.addEventListener("click", () => {
    layout.showGameScreen();
    startNewGame();
  });

  const resetBtn = document.getElementById("btn-reset");
  resetBtn?.addEventListener("click", () => {
    startNewGame();
  });

  startNewGame();
}

init();

// ---------------------------
// GAME FLOW
// ---------------------------

function startNewGame() {
  board = createEmptyBoard();
  isPlayerTurn = true;
  gameOver = false;

  layout.setStatus("Your move");
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
  if (winner) {
    endGame(winner);
    return;
  }

  isPlayerTurn = false;
  layout.setStatus("Computer is thinking…");

  // Лёгкая задержка для эффекта "думает"
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
  if (winner) {
    endGame(winner);
    return;
  }

  isPlayerTurn = true;
  layout.setStatus("Your move");
}

// ---------------------------
// GAME END HANDLING
// ---------------------------

async function endGame(winner: Winner) {
  gameOver = true;
  boardView.setEnabled(false);

  if (winner === PLAYER) {
    layout.setStatus("You win!");

    // отправляем результат
    const promo = await sendGameResult("win");

    // если backend не вернул — fallback
    const finalCode =
      promo ?? Math.floor(Math.random() * 100000).toString().padStart(5, "0");

    promoModal.show(finalCode);
    return;
  }

  if (winner === BOT) {
    layout.setStatus("You lose");

    await sendGameResult("lose");
    layout.showLoseScreen();
    return;
  }

  // draw
  layout.setStatus("Draw! Tap Play Again to restart.");
}
