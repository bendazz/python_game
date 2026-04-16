import random
from typing import Optional
from fastapi import FastAPI, Cookie, Response
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/spec", response_class=PlainTextResponse)
def get_spec():
    with open("SPEC.md", "r") as f:
        return f.read()

@app.get("/guess")
def guess(
    n: int,
    response: Response,
    secret: Optional[int] = Cookie(None),
    count: Optional[int] = Cookie(None),
):
    if secret is None:
        secret = random.randint(1, 100)
        count = 0
    count = (count or 0) + 1

    if n < secret:
        result = "higher"
    elif n > secret:
        result = "lower"
    else:
        result = "correct"

    response.set_cookie("secret", str(secret))
    response.set_cookie("count", str(count))
    return {"result": result, "count": count}

@app.post("/new_game")
def new_game(response: Response):
    new_secret = random.randint(1, 100)
    response.set_cookie("secret", str(new_secret))
    response.set_cookie("count", "0")
    return {"message": "new number picked"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
