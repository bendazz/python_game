async function submitGuess() {
    let n = document.getElementById("guess").value;
    if (n === "") return;
    let response = await fetch("/guess?n=" + n);
    let data = await response.json();

    document.getElementById("counter").textContent = "Guesses: " + data.count;

    let msg = document.getElementById("message");
    msg.className = data.result;
    if (data.result === "higher") {
        msg.textContent = "Try higher!";
    } else if (data.result === "lower") {
        msg.textContent = "Try lower!";
    } else {
        msg.textContent = "Correct! You got it in " + data.count + " guesses!";
        document.getElementById("guess-btn").disabled = true;
    }
    plotGuess(n, data.result);
}

function plotGuess(n, result) {
    let numberline = document.getElementById("numberline");
    let dot = document.createElement("div");
    dot.className = "guess-dot " + result;
    let percent = ((n - 1) / 99) * 100;
    dot.style.left = percent + "%";
    dot.textContent = n;
    numberline.appendChild(dot);
}

async function resetGame() {
    await fetch("/new_game", { method: "POST" });
    document.getElementById("counter").textContent = "Guesses: 0";
    let msg = document.getElementById("message");
    msg.textContent = "New game! Make a guess.";
    msg.className = "";
    document.getElementById("guess").value = "";
    document.getElementById("guess-btn").disabled = false;
    let dots = document.querySelectorAll(".guess-dot");
    for (let i = 0; i < dots.length; i++) {
        dots[i].remove();
    }
}
