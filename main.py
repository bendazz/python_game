import random
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/spec", response_class=PlainTextResponse)
def get_spec():
    with open("SPEC.md", "r") as f:
        return f.read()

secret_number = random.randint(1, 100)
guess_count = 0

@app.get("/guess")
def guess(n: int):
    global guess_count
    guess_count = guess_count + 1
    if n < secret_number:
        return {"result": "higher", "count": guess_count}
    if n > secret_number:
        return {"result": "lower", "count": guess_count}
    return {"result": "correct", "count": guess_count}

@app.post("/new_game")
def new_game():
    global secret_number, guess_count
    secret_number = random.randint(1, 100)
    guess_count = 0
    return {"message": "new number picked"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
