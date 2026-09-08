# Streamlit · 01 — Introduction: What, Why, and Your First App

**Time:** ~45 min · **CLOs:** CLO-1, CLO-3 · **Level:** Beginner

---

## 1. What is Streamlit?

Streamlit is a free, open-source Python library that **turns a Python script
into a web app**. You write normal Python — `st.title(...)`, `st.write(...)`,
`st.selectbox(...)` — save it as `app.py`, and run:

```bash
streamlit run app.py
```

A browser tab opens with a working, clickable application. No HTML, no CSS,
no JavaScript, no web server code. **If you can write a Python script, you
can build a web app.**

## 2. Why do data scientists use it?

- **Speed** — an interactive dashboard takes minutes, not days. The script
  *is* the app.
- **No web skills needed** — everything you already learned (pandas,
  Matplotlib, scikit-learn) works inside the app unchanged.
- **Interactivity for free** — add one widget (`st.slider`) and your whole
  analysis becomes filterable. No JavaScript.
- **Sharing** — apps run on your machine locally; the same script can later
  be deployed to a free hosting service (basic deployment, document 7).

The professional workflow it enables: you explore data in a notebook, then
wrap the *findings* in an app so non-programmers (managers, classmates,
clients) can explore them too. **The notebook is for you; the app is for
your audience.**

## 3. Installation

```bash
pip install streamlit
```

Verify it worked:

```bash
streamlit hello
```

A demo app opens in your browser. If you see it, Streamlit is installed.
Stop it with `Ctrl+C` in the terminal (or close the window). We won't need
the demo again.

> **Troubleshooting:** `streamlit: command not found` → your Python scripts
> folder isn't on PATH. With a virtual environment, activate it first
> (`.venv\Scripts\activate` on Windows, `source .venv/bin/activate` on
> macOS/Linux), or run `python -m streamlit hello` instead.

## 4. Running an app — the three things that happen

1. **You run `streamlit run app.py`** — a local server starts (default
   http://localhost:8501) and opens your browser.
2. **Streamlit executes your script from top to bottom** — every line runs,
   in order. That's the whole "framework": top-to-bottom execution.
3. **You interact** (click a button, move a slider) — Streamlit
   **re-runs the entire script** with the new widget value. This is called a
   **rerun**, and understanding it explains almost everything about
   Streamlit (see the FAQ, question 1).

```text
  streamlit run app.py
        │
        ▼
  your script runs top to bottom ──► page appears in the browser
        │
        ▲            user clicks / moves a widget
        └──────────── script RE-RUNS with the new values
```

## 5. Basic app structure

A Streamlit app is just a script with **text elements** and, later, widgets:

```python
import streamlit as st

st.title("My first app")          # big heading
st.header("A section heading")    # medium heading
st.subheader("Smaller heading")   # smaller heading
st.write("Hello! Streamlit shows this as text.")
st.markdown("**Bold** and *italic* work here too.")
```

| Element | What it looks like | When to use it |
|---|---|---|
| `st.title` | large page title | once, at the top |
| `st.header` | section heading | to split the page into parts |
| `st.subheader` | sub-section heading | sub-parts of a section |
| `st.write` | smart text/code/data | everything else — it guesses how to display its argument |
| `st.markdown` | formatted text | when you need bold, italics, lists, or links |

`st.write` is the most useful: give it a string, a number, a dataframe, or a
plot — it decides how to display it. Use the others when you want *control*
over the look.

---

# Example 1 — Hello Data Science

The smallest complete app. It explains itself.

## Explanation

Three parts: a title, a short introduction, and one line that proves the app
is *live* (Python computes something and Streamlit displays it — the app is
real code, not a static page).

## Code

Save as `app.py`:

```python
import streamlit as st

# Part 1 — title and intro
st.title("👋 Hello Data Science")
st.header("My first Streamlit app")
st.markdown("This app is built with **pure Python** — no HTML or CSS needed.")

# Part 2 — Python runs inside the app
name = "Data Science student"
st.write(f"Welcome, {name}!")

# Part 3 — live computation (re-runs every time you interact)
number = 2 + 2
st.write(f"Streamlit can compute: 2 + 2 = {number}")
st.success("The app is running. You are looking at a live Python program!")
```

## Expected result

```
👋 Hello Data Science
My first Streamlit app
This app is built with pure Python — no HTML or CSS needed.
Welcome, Data Science student!
Streamlit can compute: 2 + 2 = 4
✅ The app is running. You are looking at a live Python program!
```

Your browser shows the heading, the text, and the green success message.
Because Streamlit runs the script live, even this trivial app is *real
Python executing in your browser tab*.

## Exercise

1. Change `name` to your own name and re-run the app (Streamlit shows a
   "Rerun" button in the top-right when the file changes — click it, or
   just refresh).
2. Add a line using `st.header("About this course")` below the title.
3. Add an `st.markdown` line that renders a bullet list of three things you
   learned in Module A (e.g. `- pandas`, `- NumPy`, `- Matplotlib`).

## Challenge

Display today's date and the number of days left in the 16-week semester
using Python's `datetime` module inside the app:

```python
import datetime

today = datetime.date.today()
# semester started, say, Jan 5 — compute days left however you like
st.write(f"Today is {today}.")
```

Make it compute the day of the week too (`today.strftime("%A")`).

---

## Common mistakes (introduction)

| Mistake | Fix |
|---|---|
| `streamlit: command not found` | activate your virtual environment first |
| App runs but browser doesn't open | the URL is printed in the terminal — open it manually |
| Changes don't appear | Streamlit detects file saves — click **Rerun** in the app or refresh |
| `ModuleNotFoundError: streamlit` | you installed into a different Python environment — install into the one you run |
| Port 8501 already in use | `streamlit run app.py --server.port 8502` |

## Checkpoint questions

1. What command starts a Streamlit app? *(CLO-1 · Understand · Easy)*
   **Answer:** `streamlit run app.py`.
2. What happens to your script every time the user interacts with a widget?
   *(CLO-1 · Understand · Easy)*
   **Answer:** the entire script re-runs from top to bottom (a rerun).
3. Why do data scientists use Streamlit instead of building websites with
   HTML/CSS/JS? *(CLO-3 · Evaluate · Medium)*
   **Answer:** it needs no web skills, reuses the Python data stack
   directly, and produces interactive apps in minutes — the notebook is for
   exploration, the app is for the audience.