async function loadBoard() {
    let response = await fetch("/board");
    let board = await response.json();
    let boardDiv = document.getElementById("board");
    boardDiv.innerHTML = "";
    for (let i = 0; i < board.length; i++) {
        let cell = document.createElement("div");
        cell.className = "cell";
        cell.textContent = board[i];
        cell.addEventListener("click", function () {
            makeMove(i);
        });
        boardDiv.appendChild(cell);
    }

    let playerResponse = await fetch("/current_player");
    let player = await playerResponse.json();
    document.getElementById("turn").textContent = "Current turn: " + player;
}

async function makeMove(position) {
    let response = await fetch("/move?position=" + position, {
        method: "POST"
    });
    let result = await response.json();
    if (result.error) {
        document.getElementById("message").textContent = result.error;
    } else {
        document.getElementById("message").textContent = "";
    }
    loadBoard();
}

async function resetGame() {
    await fetch("/reset", { method: "POST" });
    document.getElementById("message").textContent = "";
    loadBoard();
}

loadBoard();
