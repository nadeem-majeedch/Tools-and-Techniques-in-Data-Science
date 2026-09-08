# Lab 01 — What is Data Science? & Environment Setup

**Session:** Week 1 · Session 1 · 90 min
**CLO:** CLO-1 (foundation)
**Difficulty:** Beginner

## Learning objectives

By the end of this lab you can:

1. Explain the data science lifecycle in your own words.
2. Verify your Python, Jupyter, Git, and editor installation.
3. Create and activate a virtual environment.
4. Run your first Python + pandas + NumPy code.
5. Start a course repository on GitHub and clone it locally.

## Problem statement

A new hire at a data team needs a working, verifiable environment on day
one. Your task: prove that **your machine** can run the exact software stack
this course uses — nothing more, nothing less — and record the proof.

## Dataset requirements

None — you generate a tiny dataset inline (a list of numbers).

## Step-by-step tasks

1. **Check versions.** Open a terminal and run the checks in the starter
   code below. Record every version you get.
2. **Create a virtual environment** named `.venv` in your course folder and
   activate it. (If you already did this in the session, record the command.)
3. **Install the course stack** with `pip install -r requirements.txt`
   (the file is at the repository root). Note how long it takes.
4. **Run the smoke test** below inside the environment. It must print
   versions of pandas and NumPy and the mean of `[2, 4, 6, 8]`.
5. **Create a GitHub repo** named `data-science-course`, clone it locally,
   and commit a first `hello.md` file. Push it.
6. **Write a short paragraph** in `hello.md`: name the 5 stages of the data
   science lifecycle and which course module covers each.

## Starter code

```python
# smoke_test.py — run inside your activated virtual environment
import sys
import numpy as np
import pandas as pd

print("Python:", sys.version.split()[0])
print("NumPy:", np.__version__)
print("pandas:", pd.__version__)

numbers = [2, 4, 6, 8]
print("mean of", numbers, "=", np.mean(numbers))
```

```bash
# terminal checks (record all output)
python --version
git --version
jupyter --version
```

## Expected output

```
Python: 3.x.y
NumPy: 2.x.y
pandas: 2.x.y
mean of [2, 4, 6, 8] = 5.0
```

(Exact versions depend on your machine — the point is that all three print
without errors.)

## Questions

1. List the five stages of the data science lifecycle.
2. Which stage is this course's Module A about? Module B? Module C?
3. Why use a virtual environment instead of installing packages globally?
4. What does `git push` do, and why do teams use GitHub?
5. True/False: Jupyter is a programming language.

## Challenge task

Write a `versions.md` file that records your Python, NumPy, pandas, Git,
and Jupyter versions as a table, plus the date. Commit and push it. This
file is your machine's "baseline" — you will reuse it in Lab 24
(Reproducible Workflows).

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Versions recorded for all five tools | 2 | from `versions.md` table |
| Virtual environment created & used | 2 | `.venv` in repo, smoke test ran in it |
| Smoke test runs without errors | 3 | correct output `mean = 5.0` |
| GitHub repo cloned & first commit pushed | 2 | commit message meaningful |
| Lifecycle paragraph (5 stages + module map) | 3 | each stage named correctly |
| Challenge: `versions.md` committed | 3 | table + date |
| **Total** | **15** | |