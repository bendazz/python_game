from typing import Optional
from fastapi import FastAPI, Cookie, Response
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

WIDTH = 8
HEIGHT = 6


def build_grid(row, col):
    grid = []
    for r in range(HEIGHT):
        row_list = []
        for c in range(WIDTH):
            row_list.append(0)
        grid.append(row_list)
    grid[row][col] = 1
    return grid


@app.get("/spec", response_class=PlainTextResponse)
def get_spec():
    with open("SPEC.md", "r") as f:
        return f.read()


@app.get("/state")
def get_state(
    response: Response,
    row: Optional[int] = Cookie(None),
    col: Optional[int] = Cookie(None),
):
    if row is None:
        row = 0
    if col is None:
        col = 0
    grid = build_grid(row, col)
    response.set_cookie("row", str(row))
    response.set_cookie("col", str(col))
    return {"grid": grid, "row": row, "col": col, "width": WIDTH, "height": HEIGHT}


@app.post("/step")
def step(
    response: Response,
    row: Optional[int] = Cookie(None),
    col: Optional[int] = Cookie(None),
):
    if row is None:
        row = 0
    if col is None:
        col = 0
    col = col + 1
    if col >= WIDTH:
        col = 0
        row = row + 1
    if row >= HEIGHT:
        row = 0
    grid = build_grid(row, col)
    response.set_cookie("row", str(row))
    response.set_cookie("col", str(col))
    return {"grid": grid, "row": row, "col": col}


@app.post("/reset")
def reset(response: Response):
    row = 0
    col = 0
    grid = build_grid(row, col)
    response.set_cookie("row", str(row))
    response.set_cookie("col", str(col))
    return {"grid": grid, "row": row, "col": col}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
