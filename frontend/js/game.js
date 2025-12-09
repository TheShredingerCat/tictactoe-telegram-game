// =======================================
// TELEGRAM GAME PLATFORM
// =======================================

let userId = null;

window.addEventListener("load", () => {
    const params = window.TelegramGameProxy?.initParams;

    if (params && params.user) {
        userId = params.user.id;
        console.log("Telegram User ID:", userId);
    } else {
        console.warn("Game opened outside Telegram — no userId available");
    }
});


// =======================================
// UI ELEMENTS
// =======================================

const boardElement = document.getElementById('board');
const statusText = document.getElementById('statusText');
const btnNewGame = document.getElementById('btnNewGame');
const btnPlayAgain = document.getElementById('btnPlayAgain');

const promoBlock = document.getElementById('promoBlock');
const promoCodeElement = document.getElementById('promoCode');

const bannerWin = document.getElementById('bannerWin');
const bannerLose = document.getElementById('bannerLose');
const bannerDraw = document.getElementById('bannerDraw');


// =======================================
// GAME STATE
// =======================================

let board = Array(9).fill(null);
let gameOver = false;

const PLAYER = "X";
const BOT = "O";

const cells = [];


// =======================================
// BOARD CREATION
// =======================================

for (let i = 0; i < 9; i++) {
    const cell = document.createElement("div");
    cell.className = "cell";
    cell.dataset.index = i;

    const content = document.createElement("div");
    content.className = "cell-content";
    cell.appendChild(content);

    cell.addEventListener("click", () => handlePlayerMove(i));

    boardElement.appendChild(cell);
    cells.push(cell);
}


// =======================================
// RESET GAME
// =======================================

function resetGame() {
    board = Array(9).fill(null);
    gameOver = false;

    cells.forEach(cell => {
        cell.classList.remove("disabled", "winning");
        const cont = cell.querySelector(".cell-content");
        cont.textContent = "";
        cont.classList.remove("player", "bot");
    });

    bannerWin.style.display = "none";
    bannerLose.style.display = "none";
    bannerDraw.style.display = "none";
    promoBlock.style.display = "none";

    statusText.textContent = "Ваш ход";
}

btnNewGame.addEventListener("click", resetGame);
btnPlayAgain.addEventListener("click", resetGame);


// =======================================
// PLAYER MOVE
// =======================================

function handlePlayerMove(index) {
    if (gameOver || board[index] !== null) return;

    placeMark(index, PLAYER);

    const resultObj = checkGameEnd();
    if (resultObj) {
        return endGame(resultObj);
    }

    statusText.textContent = "Бот думает…";
    disableBoard();

    setTimeout(() => {
        botMove();
        const resultObj2 = checkGameEnd();
        if (resultObj2) {
            return endGame(resultObj2);
        }
        enableBoard();
        statusText.textContent = "Ваш ход";
    }, 500);
}


// =======================================
// PLACE MARK
// =======================================

function placeMark(index, player) {
    board[index] = player;

    const cell = cells[index];
    const content = cell.querySelector(".cell-content");

    content.textContent = player === PLAYER ? "✕" : "◯";
    content.classList.add(player === PLAYER ? "player" : "bot");

    cell.classList.add("disabled");
}

function disableBoard() {
    cells.forEach(c => c.classList.add("disabled"));
}

function enableBoard() {
    if (gameOver) return;
    board.forEach((val, i) => {
        if (val === null) cells[i].classList.remove("disabled");
    });
}


// =======================================
// BOT MOVE (simple AI)
// =======================================

function botMove() {
    const empty = board
        .map((v, i) => (v === null ? i : null))
        .filter(v => v !== null);

    const move = empty[Math.floor(Math.random() * empty.length)];
    placeMark(move, BOT);
}


// =======================================
// CHECK GAME END (returns object)
// =======================================

function checkGameEnd() {
    const wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6],
    ];

    for (const line of wins) {
        const [a, b, c] = line;

        if (board[a] && board[a] === board[b] && board[b] === board[c]) {
            return {
                winner: board[a] === PLAYER ? "player" : "bot",
                line
            };
        }
    }

    if (board.every(cell => cell !== null)) {
        return {
            winner: "draw",
            line: []
        };
    }

    return null;
}


// =======================================
// END GAME (resultObj = {winner, line})
// =======================================

async function endGame(resultObj) {
    gameOver = true;
    disableBoard();

    // подсветка победной линии
    if (resultObj.winner !== "draw") {
        resultObj.line.forEach(i => {
            cells[i].classList.add("winning");
        });
    }

    // запрос на backend
    let promoFromServer = null;
    let achievement = null;

    if (userId) {
        try {
            const resp = await fetch("http://localhost:9000/api/game-result", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    userId,
                    result: resultObj.winner,
                    promoCode: null
                })
            });

            if (resp.ok) {
                const data = await resp.json();
                promoFromServer = data.promoCode || null;
                achievement = data.achievement || null;
            }
        } catch (err) {
            console.error("Ошибка связи с backend:", err);
        }
    }

    // UI for result
    if (resultObj.winner === "player") {
        promoBlock.style.display = "flex";

        promoCodeElement.textContent =
            promoFromServer ?? generateFallbackPromo();

        bannerWin.style.display = "block";
        statusText.textContent = "Вы победили!";
    }

    else if (resultObj.winner === "bot") {
        bannerLose.style.display = "block";
        statusText.textContent = "Бот выиграл";
    }

    else {
        bannerDraw.style.display = "block";
        statusText.textContent = "Ничья";
    }
}


// =======================================
// FALLBACK PROMOCODE
// =======================================

function generateFallbackPromo() {
    return String(Math.floor(Math.random() * 100000)).padStart(5, "0");
}


// =======================================
// START GAME
// =======================================

resetGame();
