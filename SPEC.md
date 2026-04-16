# Number Guessing Game — Student Spec

You are going to build a small web app: a number guessing game. The player guesses a number between 1 and 100, and the app tells them whether to guess higher or lower until they get it right.

Before you start writing endpoints, here are a few short tutorials on concepts you'll need that we haven't covered in class yet.

---

## Tutorial 1: Generating a random integer

To make the game fun, the computer needs to pick a **secret number** that the player has to guess. We want that number to be different each game — not the same one every time. Python gives us a built-in tool for this called the `random` module.

### Step 1: Import the module

At the top of your Python file, write:

```python
import random
```

`import` tells Python, "I want to use code from another file called `random`." The `random` module is included with Python, so you don't have to install anything.

### Step 2: Use `random.randint`

The function we want is called `randint`, short for "random integer." You call it like this:

```python
random.randint(1, 100)
```

This returns a whole number somewhere between 1 and 100. **Both endpoints are included**, so you could get 1, you could get 100, or anything in between.

### Step 3: Save the result in a variable

Usually you want to remember the number, so store it in a variable:

```python
secret_number = random.randint(1, 100)
print(secret_number)
```

Run that a few times — you'll see a different number each time.

### Try it yourself

1. Open a Python file and write three lines that pick a random number between 1 and 10 and print it.
2. Run the file five times in a row. Did you get the same number every time? Why not?
3. Change the range so the number is between 50 and 75.

### Quick reference

| Code                       | What it does                           |
|----------------------------|----------------------------------------|
| `import random`            | Makes the `random` module available    |
| `random.randint(1, 100)`   | Returns a random whole number, 1–100   |
| `random.randint(a, b)`     | Returns a random whole number, a–b     |

---

## Tutorial 2: The `global` keyword

In this game, the secret number lives **outside** of any function — at the top of the file. That way, every endpoint can see it. A variable like this is called a **global variable**.

```python
secret_number = random.randint(1, 100)
```

There's one tricky rule about global variables that you'll run into when you write the "new game" endpoint.

### The rule

If a function only **reads** a global variable, you don't need to do anything special:

```python
secret_number = 42

def check(n):
    if n < secret_number:      # just reading — this works fine
        print("higher")
```

But if a function needs to **change** (reassign) a global variable, Python needs you to say so explicitly. You do that with the `global` keyword:

```python
secret_number = 42

def new_game():
    global secret_number                    # "I mean the one up top"
    secret_number = random.randint(1, 100)  # now this reassigns it
```

### Why is this necessary?

Without the `global` line, Python assumes any variable you assign to inside a function is a **new local variable** that only exists while the function runs. So the outside `secret_number` would never change, and every time you called `new_game()` it would look like nothing happened.

The `global` line tells Python: "When I say `secret_number` in here, I mean the one defined at the top of the file — not a new one."

### When to use it

- **Reading a global?** No `global` needed.
- **Assigning to a global?** Put `global variable_name` as the first line of the function.

### Quick reference

| Situation                                    | Do you need `global`? |
|----------------------------------------------|-----------------------|
| `if secret_number > 10:` inside a function   | No                    |
| `print(secret_number)` inside a function     | No                    |
| `secret_number = 50` inside a function       | **Yes**               |
| `secret_number = random.randint(1, 100)`     | **Yes**               |

---

## Tutorial 3: GET vs POST

So far in class we've used `@app.get` to write endpoints. There's a second one you'll need for this project: `@app.post`. Here's the difference.

### The rule

- **GET** is for **reading** data. The endpoint looks up something and returns it. It should not change anything on the server.
- **POST** is for **doing** something that **changes** state on the server — creating, updating, resetting, etc.

### Why it matters

Picking a new secret number is an action that **changes** what's stored in your app, so it should be a POST. Checking a guess just **reads** the secret number to compare it — that's a GET.

If you used GET for an action like "new game," a browser or a caching proxy could decide to pre-fetch or re-run that URL on its own, and suddenly your secret number would change at the wrong time. GETs are supposed to be safe to repeat; POSTs are not.

### How to write one

It's a one-word change to the decorator:

```python
@app.get("/guess")          # reading
def guess(n: int):
    ...

@app.post("/new_game")      # doing/changing
def new_game():
    ...
```

### How to test a POST

You can't test a POST by just typing the URL in your browser — the browser address bar only sends GET requests. Instead, take your app's homepage URL and add `/docs` to the end of it. FastAPI automatically builds a page there where you can click "Try it out" on any endpoint, GET or POST.

### Quick reference

| Use `@app.get`                   | Use `@app.post`                      |
|----------------------------------|--------------------------------------|
| Reading data                     | Doing an action                      |
| Does not change server state     | Changes server state                 |
| Safe to repeat                   | Not safe to blindly repeat           |
| Testable from the browser bar    | Test from `/docs` or the frontend    |

---

## The Endpoints

You are going to write the two endpoints that make this game work. Before you write them, put this line at the **very top of your file**, outside of any function:

```python
secret_number = random.randint(1, 100)
```

This creates the first secret number when your app starts up. Your endpoints will read it and change it.

### Endpoint 1: `/new_game`

**What it should do:** Pick a brand-new secret number between 1 and 100, so the player can start a fresh game. This is the endpoint the "New Game" button on the front end will call.

**Method:** `POST`

**Inputs:** None.

**What it returns:** A dictionary with a short message letting the player know a new number has been picked. For example:

```python
{"message": "new number picked"}
```

**Hints:**
- You are changing the value of `secret_number`, which lives outside the function. Remember Tutorial 2 — you'll need one specific keyword inside your function.
- Use `random.randint` from Tutorial 1 to pick the new number.
- The body of this function is only a few lines long. If you're writing a lot of code, you may be overcomplicating it.

**How to test it:** After you start the server, open your app's homepage and add `/docs` to the end of the URL. FastAPI gives you a page where you can click "Try it out" on any endpoint. Call `/new_game` a few times and then `print(secret_number)` in your code to confirm the number is actually changing.

### Checkpoint: See your endpoint in action

Before moving on, let's watch your new endpoint work in a real web page.

**Step 1 — Add a temporary "debug" endpoint.** Write a second endpoint called `/secret` that just returns the current value of `secret_number`:

```python
@app.get("/secret")
def get_secret():
    return {"secret": secret_number}
```

In a real game you would **never** expose the secret number to the player — but while we're building, it's the easiest way to watch things change. We'll delete this endpoint later.

**Step 2 — Ask AI to build a small front end.** Open your AI assistant and give it a prompt like:

> Build me a simple HTML page with one button labeled "New Game" and a line of text that shows the current secret number. When the button is clicked, send a POST request to `/new_game`, then fetch `/secret` and update the text with the new value. When the page first loads, also fetch `/secret` so the current number shows right away.

Save whatever it gives you into `static/index.html` (and any `.js` / `.css` files into the same folder).

**Step 3 — Try it.** Refresh your app's homepage. You should see the current secret number displayed. Click "New Game" a few times and watch the number change. If it does — your `/new_game` endpoint is working!

> Keep the `/secret` endpoint around while you build the next endpoint — it's useful for debugging. You can delete it at the end.

### Endpoint 2: `/guess`

**What it should do:** Take a number from the player and compare it to the secret number. Tell the player whether they need to guess **higher**, guess **lower**, or whether they are **correct**.

**Method:** `GET`

**Inputs:** A single whole number called `n` — the player's guess. In FastAPI, you accept a query parameter by adding it to the function's parameter list with a type:

```python
def guess(n: int):
    ...
```

That means the player will call the endpoint like this: `/guess?n=42`.

**What it returns:** A dictionary with a single key called `result`, whose value is one of three strings: `"higher"`, `"lower"`, or `"correct"`.

- If the player's guess is **less than** the secret, they need to try higher:
  ```python
  {"result": "higher"}
  ```
- If the player's guess is **greater than** the secret, they need to try lower:
  ```python
  {"result": "lower"}
  ```
- If the player's guess **equals** the secret, they got it:
  ```python
  {"result": "correct"}
  ```

**Hints:**
- This endpoint only **reads** the secret number — it doesn't change it. Look back at Tutorial 3 to pick the right decorator, and at Tutorial 2 to decide whether you need the `global` keyword in this function (you don't!).
- You'll need an `if` statement with three branches. Use `if`, `elif`, and `else`.
- Don't forget the type hint `n: int` in the function signature — without it, FastAPI won't know what kind of value to expect.

**How to test it:**
1. Open your app's homepage and add `/docs` to the URL.
2. Click on `/guess`, then "Try it out."
3. Use your `/secret` debug endpoint from the last checkpoint to peek at the current secret number.
4. Submit a guess that's **lower** than the secret — you should get `"higher"` back.
5. Submit a guess that's **higher** than the secret — you should get `"lower"` back.
6. Submit a guess that **equals** the secret — you should get `"correct"`.

If all three cases work, your endpoint is done!

---

## Extending the Game: Tracking Guesses on the Backend

Now that both endpoints work, let's add a feature: the game should keep track of **how many guesses** the player has made, and report that number back to them (so they can try to beat their own record).

You might be tempted to count the guesses on the front end — just add 1 every time the Guess button is clicked. That would work, but there's a design principle worth learning:

> **Game state belongs on the backend. Display belongs on the front end.**

The guess count is game state — it's part of the "current game" the server is running. So we'll track it on the server and let the front end just display whatever the server reports. This also means if you ever add a rule like "only 10 guesses per game," the backend will already have the number it needs to enforce it.

### Step 1: Add a new global variable

At the top of your Python file, right below `secret_number`, add:

```python
guess_count = 0
```

### Step 2: Modify `/guess`

Your `/guess` endpoint should now do two extra things:

1. **Increment `guess_count` by 1** every time it's called. (Remember Tutorial 2 — you're changing a global, so you'll need the `global` keyword.)
2. **Include the count in the response** as a new key called `count`. The response should now look like:

   ```python
   {"result": "higher", "count": 3}
   ```

### Step 3: Modify `/new_game`

When a new game starts, the guess count should go back to 0. Inside `/new_game`, you'll now need to change **two** global variables. You can list them both on one `global` line, separated by a comma:

```python
global secret_number, guess_count
```

Then set `guess_count = 0` along with picking a new secret number.

### How to test it

Open `/docs` and:

1. Call `/guess?n=50` a few times. Each response should have a larger `count` than the one before.
2. Call `/new_game`. Then call `/guess` again — the `count` should be back to 1.

Once the backend is tracking guesses, you're ready to build the final front end.

---

## Finishing the Game: The Real Front End

Both endpoints work. Time to replace the debug page with a real one.

**Step 1 — Delete the debug endpoint.** The `/secret` endpoint was only there to help you see things while building. A real guessing game would never show the player the answer! Delete the `/secret` function from your Python file.

**Step 2 — Ask AI to build the full front end.** Open your AI assistant and give it a prompt along these lines:

> Build me a simple front end for a number guessing game in `static/index.html`, with any CSS or JS files in the same folder. My FastAPI backend has two endpoints:
>
> - `GET /guess?n=<number>` — returns a dictionary with two keys: `result` (one of `"higher"`, `"lower"`, `"correct"`) and `count` (the number of guesses so far in this game).
> - `POST /new_game` — picks a new secret number and resets the guess count. Returns `{"message": "new number picked"}`.
>
> The page should have:
> - A title and short instructions ("Guess a number between 1 and 100").
> - An input box for the guess.
> - A "Guess" button that sends the guess to `/guess` and shows the result ("Try higher!", "Try lower!", or "You got it!").
> - A display showing the current guess count (updated from the `count` field in each response).
> - A "New Game" button that calls `/new_game` and clears the message and resets the displayed count to 0.
>
> Make it look clean and friendly.

**Step 3 — Try it.** Refresh your app's homepage and play the game. Try guessing too high, too low, and exactly right. Click "New Game" and play again.

### Bonus ideas

Once it works, try asking AI to add one or more of these:

- **A number line** that plots each guess as a dot, so the player can see their past guesses at a glance.
- **Color-coded messages** — red for "too high," blue for "too low," green for "correct."
- **Disable the Guess button** once the player gets the right answer, so the game ends cleanly.

Pick one, write the prompt yourself, and see how close you can get to a version you're proud of.
