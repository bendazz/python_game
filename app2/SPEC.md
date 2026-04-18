# Grid Walker — Student Spec

You are going to build a small web app: a **grid walker**. The app shows a rectangular grid of cells with a single red dot sitting in the top-left cell. Each time you click a "Step" button, the dot moves one cell to the right. When it reaches the end of a row, it jumps to the start of the next row. Finally, you'll add an "Animate" button that steps the dot automatically so it walks through the whole grid on its own.

This project is a follow-up to the number guessing game. You've already seen `@app.get`, `@app.post`, and the `global` keyword — we won't re-explain those. What's new here is **2D data**: storing a grid in Python and moving through it with nested loops.

Before you start writing endpoints, here are two short tutorials on concepts you'll need that we haven't covered in class yet.

---

## Tutorial 1: Lists of Lists (2D Grids)

So far we've used lists to hold a sequence of values:

```python
numbers = [10, 20, 30, 40]
print(numbers[2])   # 30
```

What if we want to store a **grid** of values — like a checkerboard, a spreadsheet, or in our case, the cells of a game board?

The answer is a **list of lists**. Each item in the outer list is itself a list that represents one row of the grid.

```python
grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]
```

That's a grid with 3 rows and 4 columns, where every cell holds a `0`.

### Reading and writing a cell

To get or change the value in one cell, you use **two** index operations — first the row, then the column:

```python
grid[0][0]       # the top-left cell
grid[2][3]       # the bottom-right cell (row 2, col 3)
grid[1][1] = 1   # set a cell in the middle to 1
```

The convention we'll use in this project is `grid[row][col]`. Rows go **down**, columns go **across**.

### A quick picture

```
       col 0   col 1   col 2   col 3
row 0 [  0       0       0       0  ]
row 1 [  0       0       0       0  ]
row 2 [  0       0       0       0  ]
```

So `grid[1][2]` is the cell in row 1, column 2.

### Try it yourself

```python
grid = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
grid[0][0] = 1
grid[2][2] = 1
print(grid)
```

You should see `[[1, 0, 0], [0, 0, 0], [0, 0, 1]]` — two corners flipped to 1.

### Quick reference

| Code                 | What it does                              |
|----------------------|-------------------------------------------|
| `grid[r][c]`         | Reads the cell at row `r`, column `c`     |
| `grid[r][c] = 1`     | Sets that cell to 1                       |
| `len(grid)`          | Number of rows                            |
| `len(grid[0])`       | Number of columns                         |

---

## Tutorial 2: Nested For Loops

When we have a 2D grid, we often need to visit **every cell**. One `for` loop isn't enough — we need a loop inside a loop.

```python
for r in range(3):        # outer loop: each row
    for c in range(4):    # inner loop: each column
        print(r, c)
```

This prints:

```
0 0
0 1
0 2
0 3
1 0
1 1
...
2 3
```

The inner loop runs **all the way through** for each single step of the outer loop. That's why the column numbers reset to 0 every time the row number increases.

### Building a 2D grid with nested loops

Here's how to build a grid full of 0s at the top of your program:

```python
WIDTH = 4
HEIGHT = 3

grid = []
for r in range(HEIGHT):
    row_list = []
    for c in range(WIDTH):
        row_list.append(0)
    grid.append(row_list)
```

Walk through what happens:

1. `grid` starts as an empty list.
2. The outer loop runs `HEIGHT` times — once per row.
3. Each time, we create a fresh `row_list` and the inner loop appends `WIDTH` zeros to it.
4. Then we append that finished row onto `grid`.

When the loops finish, `grid` is a 3×4 list of lists.

### Visiting every cell

The same pattern — outer loop for rows, inner loop for columns — is how you clear, fill, or inspect every cell:

```python
for r in range(HEIGHT):
    for c in range(WIDTH):
        grid[r][c] = 0
```

Remember this shape. You'll use it more than once in this project.

### Quick reference

| Pattern                                         | What it does                       |
|-------------------------------------------------|------------------------------------|
| `for r in range(H):` / `for c in range(W):`     | Visits every cell in row order     |
| `grid.append(row_list)`                         | Adds a completed row to the grid   |
| `row_list.append(0)`                            | Adds one cell to the current row   |

---

## The Endpoints

You're going to write three endpoints. Before any of them, set up the **state** that lives at the top of your file — outside any function, so every endpoint can see it.

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

WIDTH = 8
HEIGHT = 6

# Build the grid full of 0s using nested loops (see Tutorial 2)
grid = []
for r in range(HEIGHT):
    row_list = []
    for c in range(WIDTH):
        row_list.append(0)
    grid.append(row_list)

# Put the dot in the top-left cell
grid[0][0] = 1
row = 0
col = 0
```

The rules of our little world:
- `1` in a cell means "the dot is here."
- `0` means the cell is empty.
- `row` and `col` always point to the cell currently holding the dot.

> **Important:** put the `app.mount(...)` line at the **very bottom** of your file, after all of your endpoints. Otherwise FastAPI tries to match static files before your endpoints and your API will disappear.
>
> ```python
> app.mount("/", StaticFiles(directory="static", html=True), name="static")
> ```

### Endpoint 1: `/state`

**What it should do:** Return everything the front end needs to draw the grid — the grid itself, the current row and column, and the grid's dimensions.

**Method:** `GET`

**Inputs:** None.

**What it returns:** A dictionary shaped like this:

```python
{"grid": grid, "row": row, "col": col, "width": WIDTH, "height": HEIGHT}
```

**Hints:**
- This endpoint only **reads** the globals — you do **not** need the `global` keyword here.
- FastAPI turns Python lists into JSON arrays automatically, so returning `grid` directly just works.
- The whole function body is two lines.

**How to test it:** Start the server, open `/docs`, and call `/state`. The response will be the raw dictionary — a `"grid"` key whose value is a list of six lists (the rows), each with eight zeros, except for a single `1` at the very start. Something like:

```
{
  "grid": [
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ...
  ],
  "row": 0,
  "col": 0,
  "width": 8,
  "height": 6
}
```

Don't worry that it doesn't *look* like a grid yet — that's the front end's job, which we'll build in the next step.

### Checkpoint: See the grid on the page

Let's get something on screen before moving on.

**Ask AI to build a minimal front end.** Open your AI assistant and give it a prompt like:

> Build me an `index.html` (plus any CSS or JS in the same folder) that calls `GET /state` when the page loads. The response looks like:
>
> `{"grid": [[0,0,...], [0,0,...], ...], "row": 0, "col": 0, "width": 8, "height": 6}`
>
> Render the grid as a table of small square cells. In any cell whose value is 1, draw a red dot. Show the current row and column in a line of text below the grid.

Save the files into `static/` and refresh the page. You should see an 8×6 grid with a single red dot in the top-left corner. If you see that, your `/state` endpoint is working.

### Endpoint 2: `/step`

**What it should do:** Move the dot one cell to the right. When the dot reaches the end of a row, it should jump to the beginning of the next row. When it reaches the very last cell of the last row, it should wrap back around to the top-left.

**Method:** `POST` (it changes state)

**Inputs:** None.

**What it returns:** A dictionary with the same grid/row/col fields as `/state`.

**The logic, step by step:**

1. Turn **off** the current cell: `grid[row][col] = 0`
2. Add `1` to `col`.
3. **If** `col` has gone past the end of the row (`col >= WIDTH`), set `col` back to `0` and add `1` to `row`.
4. **If** `row` has gone past the bottom (`row >= HEIGHT`), set `row` back to `0`.
5. Turn **on** the new cell: `grid[row][col] = 1`.

**Hints:**
- This function **reassigns** `row` and `col`, so list them with `global row, col` at the top of the function.
- You do **not** need `global grid`, because you're modifying the contents of the list (`grid[row][col] = ...`), not reassigning `grid` itself to a new list. That's a subtle but important distinction.
- The whole body should be about 7 lines — two `if` statements and a few assignments.

**How to test it:** In `/docs`, call `/step` several times and watch `col` count up. Call it again past the end of a row and confirm `row` increases while `col` resets to 0.

### Checkpoint: A "Step" button

**Ask AI to extend the page:**

> Add a button labeled "Step" under the grid. When clicked, it should send a `POST` request to `/step` and re-render the grid using the dictionary that comes back — same shape as `/state`. Update the row/column text below the grid too.

Refresh the page, click "Step" over and over, and watch the dot walk across the grid row by row.

### Endpoint 3: `/reset`

**What it should do:** Clear the entire grid back to 0s, put the dot in the top-left, and set `row` and `col` back to 0.

**Method:** `POST`

**Inputs:** None.

**What it returns:** A dictionary with the same shape as `/state`.

**Hints:**
- You need `global row, col`.
- Use a **nested for loop** (Tutorial 2) to walk every cell of `grid` and set it to 0.
- After the loop, set `grid[0][0] = 1`, `row = 0`, `col = 0`.

**How to test it:** In `/docs`, call `/step` many times, then call `/reset`. Call `/state` afterward and confirm the dot is back in the top-left and every other cell is 0.

### Checkpoint: A "Reset" button

**Ask AI to extend the page one more time:**

> Add a button labeled "Reset" next to the Step button. When clicked, it should send a `POST` request to `/reset` and re-render the grid from the response.

Now you can step as far as you like and always return the dot to its starting position with one click.

---

## Extending the App: Animation

Your three endpoints are done. Time to turn the Step button into a real animation.

The idea: instead of you clicking Step once per cell, we let the **front end** call `/step` over and over on a timer. The backend doesn't change at all — it still just knows how to take a single step.

This is a useful pattern to recognize: the server provides the **state transition**, and the client decides **when and how often** to ask for it.

**Ask AI to add animation:**

> Add two more buttons: "Animate" and "Stop". When "Animate" is clicked, start a timer that calls `POST /step` every 200 milliseconds and re-renders the grid after each response. When "Stop" is clicked, cancel the timer. Also cancel the timer whenever the user clicks "Reset".

Play with the delay. Try 50ms for fast, 500ms for slow.

### Bonus exercises

These next two ideas are **backend** challenges — you'll modify `main.py`, not the front end. Write them yourself; don't ask AI to do them for you. The whole point is to get comfortable with 2D grids and global state. (If a bonus also needs a visual tweak, the spec will say so — that part can go to AI.)

Pick one and give it a try.

#### Bonus 1: Leave a trail

Right now, when the dot leaves a cell, `/step` sets that cell back to `0`. Change it so every cell the dot has ever visited stays marked — just with a different value so we can tell a "visited" cell from the "current" cell.

**What to change:**
- In `/step`, instead of setting the old cell to `0`, set it to `2`. Then set the new cell to `1` as before.
- `/reset` should still clear everything back to `0`.

**One small front-end update:** Your existing front end only knows to draw a dot when a cell is `1`. Ask AI for a small revision:

> In my grid renderer, cells with value `1` should still show a red dot. Also style cells with value `2` with a light pink background (no dot) so I can see the path the dot has taken.

Click Animate and watch the dot paint its own path across the grid.

#### Bonus 2: Snake traversal

Instead of always moving right and jumping back to column 0 at the end of each row, make the dot move like a snake: right through row 0, then **left** through row 1, then right through row 2, and so on.

**Hints:**
- You need to remember which direction the dot is currently moving. Add a new global at the top of the file:
  ```python
  direction = 1    # +1 means right, -1 means left
  ```
- Inside `/step`, change `col = col + 1` to `col = col + direction`.
- The "have we hit a wall?" check needs to cover **both** sides now. The dot hit a wall if `col >= WIDTH` **or** `col < 0`.
- When you hit a wall, you need to do two things: advance `row` by 1, **and** flip `direction` (so next row goes the other way). To flip, reassign `direction = -direction`. You'll also need to "back up" `col` from the wall — think about what value it should be on the next row.
- Don't forget to add `direction` to your `global` line.
- `/reset` should set `direction` back to `1` as well.

**Front end:** no changes needed. The back end still returns the same grid shape.
