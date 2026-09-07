# Session 2 — Python Refresher

**Week 1 · Session 2 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Use Python's core types (int, float, str, bool, list, dict) correctly.
- Write `if`/`elif`/`else`, `for` and `while` loops, and functions.
- Use list comprehensions as a compact alternative to loops.
- Read data from a plain text file with `open()` / `with`.
- Run a complete "question → code → answer" script in a notebook cell.

## 2. Key concepts

- Python is dynamically typed but **strict about types at runtime** — know the type you're working with.
- Strings are sequences; lists are mutable; dicts map keys to values.
- Functions are the unit of reusable logic — one function, one job.
- Comprehensions are the Pythonic way to transform lists.
- `with open(...)` guarantees files are closed even on errors.
- Indentation **is** syntax in Python.

## 3. Detailed lecture notes

**Why review Python?** Students arrive with "basic programming" from earlier
semesters. This session standardizes that baseline, because every data science
tool in this course (NumPy, Pandas, scikit-learn) is Python underneath. The goal
is fluency in ~10 core patterns, not language trivia.

**Types.** Go over `int`, `float`, `str`, `bool` as values, then the two workhorse
collections: `list` (ordered, mutable, indexed) and `dict` (key→value lookup).
Why does this matter for data science? A DataFrame (session 7) is conceptually a
list of rows plus a dict of named columns — knowing lists and dicts makes Pandas
intuitive.

**Control flow.** `if` for decisions, `for` for repetition, `range()` for numeric
loops, `while` sparingly (easy to write infinite loops). Show the same task done
with a loop and with a comprehension, and let students feel that the comprehension
is shorter *and* more readable once you're used to it.

**Functions.** `def name(parameters): ... return value`. Emphasize: functions let
you name a piece of logic and reuse it — the seed of reproducibility (a pipeline
step later). Use `def` with sensible names; show default parameter values.

**Reading files.** Data science starts when data lives outside your code. `with
open("file.csv") as f:` reads line by line. Show manual CSV parsing here *without*
Pandas — this motivates why Pandas exists ("look how much code this is — Pandas
will do it in one line in session 8").

**Notebook mechanics reminder.** Shift+Enter runs a cell; the last expression is
printed automatically; `print()` for explicit output. Errors in one cell do not
kill the kernel — a superpower and a trap (stale variables persist).

## 4. Important terminology

- **Type** — the kind of a value: `int`, `float`, `str`, `bool`, `list`, `dict`.
- **Mutable** — changeable in place (lists, dicts) vs. immutable (strings, tuples).
- **Iterate** — process each element of a sequence one at a time.
- **Function** — named, reusable block of code with inputs (parameters) and an output (`return`).
- **Comprehension** — compact syntax to build a new list/dict from an existing one.
- **Index / slice** — position-based access; `s[0]` first element, `s[1:3]` a range.
- **F-string** — `f"{value}"` string formatting (Python 3.6+).
- **Exception** — an error the program reports instead of silently doing the wrong thing.

## 5. Python examples

```python
# --- Types ---
name = "Ayesha"
age = 20
gpa = 3.6
is_enrolled = True
scores = [88, 92, 76]
student = {"name": name, "age": age, "gpa": gpa}

print(type(age), type(gpa), type(scores), type(student))
print(student["name"])                     # dict lookup by key

# --- Control flow ---
for score in scores:
    if score >= 90:
        print("A", score)
    elif score >= 80:
        print("B", score)
    else:
        print("C", score)

# --- Function ---
def average(nums):
    """Return the mean of a list of numbers."""
    return sum(nums) / len(nums)

print(average(scores))

# --- Comprehension: keep only passing scores ---
passing = [s for s in scores if s >= 80]
print(passing)

# --- Reading a text file ---
with open("resources/example/names.txt") as f:      # one name per line
    names = [line.strip() for line in f]
print(names)
```

## 6. Beginner example

```python
# Smallest possible: greet a user by name
def greet(name):
    return f"Hello, {name}!"

print(greet("Data Science"))
```

Every concept from this session appears in one line each: string, f-string,
function, `return`, `print`.

## 7. Practical Data Science example

```python
# Temperatures (in Celsius) recorded over 7 days — a real pattern: clean + summarize
temps = [31.2, 30.1, 28.9, None, 29.5, 33.0, 32.1]  # None = missing measurement

# Step 1: clean — drop missing values
clean = [t for t in temps if t is not None]

# Step 2: summarize
print("Days measured:", len(clean))
print("Average temp:", round(sum(clean) / len(clean), 2))
print("Hottest day:", max(clean))
print("Days above 30°C:", sum(1 for t in clean if t > 30))
```

Show that this tiny pipeline is the *same shape* as a real one: acquire → clean →
summarize. In sessions 9–10, Pandas does this on 10,000-row datasets in three
lines.

## 8. In-class activity (50 min)

Create `notebooks/week-01/session-02-python-refresher.ipynb` and work through it:

1. **Warm-up (10 min):** with a partner, predict the output of 3 short snippets
   (types, slicing, dict access) — then run them.
2. **Guided exercises (25 min):** (a) compute the average of a list of prices and
   count prices above a threshold; (b) write a `count_vowels` function; (c) read a
   small file with one number per line and sum it.
3. **Mini-pipeline (15 min):** reproduce the practical example above with a
   different variable (e.g., daily study minutes) and add a `while` loop version
   of the loop.

## 9. Lab exercise

No graded lab this session (Lab 1 starts after NumPy, Session 6). The checkpoint
for this week: your notebook from the in-class activity runs top-to-bottom via
**Run All** and is committed to your personal GitHub repo (setup from Session 1's
homework). If Git feels shaky, Session 4 fixes that — commit anyway.

## 10. Common mistakes

- `= ` vs `==` — assignment vs. comparison. The single most common beginner bug.
- Forgetting `int()`/`float()` when reading numbers from a file → string arithmetic ("5"+"3" = "53").
- Modifying a list while iterating over it (`for x in lst: lst.remove(x)`) → skipped elements. Build a new list instead.
- Slicing confusion: `s[1:3]` includes index 1 but **not** 3.
- Infinite `while` loops — always ensure the condition eventually becomes False.
- Assuming a notebook cell's variables reset each run — they persist; re-run top cells after editing.

## 11. Short assessment questions

1. What does `type([1, 2])` return?
2. Rewrite `result = []` + `for i in range(5): result.append(i * 2)` as a comprehension.
3. What is wrong with `if x = 5:`?
4. Why use `with open(...)` instead of `f = open(...)` alone?
5. Given `s = "datascience"`, what is `s[0:4]` and `s[-3:]`?
6. Write a function `is_even(n)` returning True/False.

## 12. CLO mapping

CLO-1: Python fluency is the enabling skill for acquiring, cleaning, manipulating,
and exploring datasets. Without this baseline, every later Pandas/NumPy pattern
adds cognitive load. This session is the "Apply Python" foundation of CLO-1.

## 13. Suggested homework

- Finish all in-class exercises; commit the notebook to your repo.
- Practice: solve 5 exercises from any Python beginner course on strings, lists, dicts, functions (e.g., Python's own tutorial).
- Read: *Python for Data Analysis* (McKinney), chapter 2 (Python language basics) — skim, don't memorize.
- Preview: open `sns.load_dataset("tips")` in a scratch notebook and run `.head()` — you'll understand it fully by Session 7.