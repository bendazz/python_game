from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI   

app = FastAPI()

board = ["", "", "", "", "", "", "", "", ""]
current_player = "X"

@app.get("/board")
def get_board():
    return board

@app.get("/current_player")
def get_current_player():
    return current_player

@app.post("/move")
def make_move(position: int):
    global current_player
    if board[position] != "":
        return {"error": "Cell already taken"}
    board[position] = current_player
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"
    return board

@app.post("/reset")
def reset():
    global current_player
    for i in range(len(board)):
        board[i] = ""
    current_player = "X"
    return board

app.mount("/", StaticFiles(directory="static", html=True), name="static")