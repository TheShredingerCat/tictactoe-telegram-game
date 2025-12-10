import { Board, Winner } from "./core/types";
import {
  createEmptyBoard,
  makeMove,
  checkWinner,
} from "./core/gameEngine";

import { PLAYER, BOT, chooseBotMove } from "./core/botAI";
import { boardView } from "./ui/boardView";
import { layout } from "./ui/layout";
import { winScreen } from "./ui/modals";
import { sendGameResult } from "./telegram/apiClient";

// STATE
let board: Board = createEmptyBoard();
let isPlayerTurn = true;
let gameOver = false;

// INIT
function init() {
  boardView.initClickListeners();

  boardView.onCellClick((index) => {
    handlePlayerMove(index);
  });

  document.getElementById("btn-reset")?.addEventListener("click", () => {
    startNewGame();
  });

  document.getElementById("btn-lose-again")?.addEventListener("click", () => {
    layout.showGameScreen();
    startNewGame();
  });

  startNewGame();
}

init();

// GAME
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
  if (winner) return endGame(winner);

  isPlayerTurn = false;
  layout.setStatus("Computer is thinking…");

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
  layout.setStatus("Your move");
}

// END GAME
async function endGame(winner: Winner) {
  gameOver = true;
  boardView.setEnabled(false);

  if (winner === PLAYER) {
    layout.setStatus("You win!");

    const promo = await sendGameResult("win");
    const code = promo ?? "00000";

    winScreen.show(code);
    return;
  }

  if (winner === BOT) {
    layout.setStatus("You lose");

    await sendGameResult("lose");
    layout.showLoseScreen();
    return;
  }

  layout.setStatus("Draw! Tap Play Again");
}
