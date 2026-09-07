# Session 3 — Jupyter in Depth

**Week 2 · Session 3 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Explain why notebooks are the standard tool for data science exploration.
- Use markdown cells to structure a notebook (headings, lists, code blocks, images).
- Use the core magic commands: `%matplotlib inline`, `%timeit`, `%run`, `%%writefile`.
- Keep a notebook reproducible: sensible order, Run All clean, no stale state.
- Convert a notebook to HTML/PDF for submission and sharing.

## 2. Key concepts

- A notebook is a **document** (text + code + results), not just a code file.
- Two cell types: **Code** (executes) and **Markdown** (documents).
- State persists across cells — order matters, and re-running out of order breaks reproducibility.
- Magic commands (`%`) are notebook superpowers for timing, saving, and embedding.
- The kernel is the Python process behind the notebook; restart it when state is confused.

## 3. Detailed lecture notes

**Why notebooks?** Real data analysis is *iterative*: you peek, try, inspect,
correct. A notebook lets you do that while leaving a readable record of exactly
what you did — code, output, and written reasoning side by side. That record is
the heart of reproducibility (a CLO-3 theme) and of communicating results (the
final lifecycle stage). A script that just prints numbers is a worse story than a
notebook with a chart and a sentence explaining it.

**Cells.** Code cells hold executable statements; Shift+Enter runs the current
cell and advances. Markdown cells hold documentation: `#` headings, `-` lists,
`**bold**`, `` `code` ``, and `![alt](url)` images. Rule: **every analysis step
should be preceded by a markdown cell saying what you're doing and why.** That
"why" is what makes a notebook teachable and auditable.

**State and order.** Emphasize with a live demo: define `x = 5` in cell 1, use it
in cell 10, then go back and change cell 1 to `x = 10` — cell 10 still sees the
old value until re-run. This is the #1 cause of "it worked before" mysteries.
Best practice: after editing an early cell, **Kernel → Restart & Run All**.

**Magics.** `%matplotlib inline` embeds charts in the notebook (matplotlib
defaults to a separate window otherwise). `%timeit` measures how long a statement
takes — great for comparing solutions. `%%time` times a whole cell. `%run script.py`
executes an external script into the notebook namespace. `%%writefile` saves the
cell content to a file — useful for exporting a helper function. `?` and `??`
show help/source: `df.head?`.

**Notebook hygiene checklist** (write on the board): clear outputs before
submission? `Kernel → Restart & Run All` produces no errors? No absolute paths?
Seed set wherever randomness is used? Cells kept small with markdown labels?
This checklist reappears in the grading rubric for labs and assignments.

## 4. Important terminology

- **Kernel** — the Python interpreter executing notebook cells.
- **Cell** — one unit of a notebook: code or markdown.
- **Markdown** — lightweight text formatting syntax.
- **Magic command** — notebook special commands starting with `%` (line) or `%%` (cell).
- **Namespace / state** — all variables currently defined in the kernel.
- **Run All** — execute every code cell top-to-bottom (the reproducibility check).
- **Stale output** — output that no longer matches the code after edits.
- **Checkpoint** — autosaved notebook version Jupyter keeps for recovery.

## 5. Python examples

```python
# --- Timing: compare two ways to sum squares ---
%timeit sum(i * i for i in range(10000))
%timeit sum([i * i for i in range(10000)])

# --- Get help on a function without leaving the notebook ---
# run in a cell:  len?   or   len??

# --- Save a reusable helper to a file, then import it ---
%%writefile helpers.py
def square(x):
    return x * x

import helpers
print(helpers.square(7))

# --- Run an external script and bring its variables into the notebook ---
# %run helpers.py
```

```python
# --- Stale-state trap (demo, not to be copied blindly) ---
x = 5        # cell A
print(x * 2) # cell B -> 10
# Now edit cell A to x = 100 but DON'T re-run it; cell B still prints 10.
# Fix: Kernel -> Restart & Run All
```

## 6. Beginner example

```python
# One markdown cell:
#   ## My first analysis
#   The tips dataset records restaurant bills and tips.

# One code cell:
import seaborn as sns
tips = sns.load_dataset("tips")
tips.head()
```

That's a complete, reproducible notebook fragment: documented, executed, output visible.

## 7. Practical Data Science example

```python
# A realistic notebook skeleton for "Are weekend tips larger?"
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

# 1. Acquire
tips = sns.load_dataset("tips")

# 2. Explore: average tip by day
avg_tip_by_day = tips.groupby("day")["tip"].mean()

# 3. Visualize (sessions 13-14 teach this fully)
avg_tip_by_day.plot(kind="bar")
plt.title("Average tip by day of week")
plt.show()

# 4. Communicate in markdown below the chart:
# "Tips are highest on Friday in this sample — next step is to check
#  whether this holds after controlling for party size."
```

Show that the notebook *is* the deliverable: a colleague can read the story,
re-run it, and trust the numbers.

## 8. In-class activity (50 min)

Build `notebooks/week-02/session-03-jupyter-hygiene.ipynb`:

1. **Markdown first (10 min):** write a title, a "Goal" paragraph, and a bullet
   list of the steps you'll take — before writing any code.
2. **Code + magic (20 min):** load `tips`; use `%timeit` on two ways of computing
   the mean tip; use `?` on one method; embed a simple chart with `%matplotlib inline`.
3. **Break it (10 min):** deliberately reorder cells to create stale state, then
   fix with **Restart & Run All**. This makes the trap unforgettable.
4. **Submission drill (10 min):** File → Download as → HTML; confirm the HTML opens
   with all outputs. This is how several labs will be submitted.

## 9. Lab exercise

No graded lab this session. Deadline-adjacent checkpoint: all notebooks so far
(session 2 and 3) pass the hygiene checklist and are committed to your GitHub
repo. Session 4 teaches the Git workflow properly — until then, commit with the
commands from the homework sheet.

## 10. Common mistakes

- Not running **Restart & Run All** before submission → stale outputs, hidden errors.
- Long, multi-purpose cells → hard to debug and hard to read. One idea per cell.
- Absolute paths like `C:\Users\...\data.csv` → notebook breaks on another machine. Use relative paths.
- Forgetting `%matplotlib inline` → charts open in separate windows or never appear.
- Confusing the notebook's saved file with the executed state — the file stores output only if you save after running.
- Using magic commands in plain `.py` scripts — they are notebook-only.

## 11. Short assessment questions

1. What does Shift+Enter do?
2. What is the difference between `%timeit` and `%%time`?
3. Why does a notebook sometimes show wrong results after you edit an early cell?
4. Name the two cell types and what each is for.
5. What command re-runs a notebook top-to-bottom in one step?
6. True/False: variables defined in one code cell are available in later cells. (True — and that's why order matters.)

## 12. CLO mapping

CLO-1: notebooks are the working surface for acquiring, cleaning, exploring data
all semester. The hygiene skills here are also the first reproducibility habits
(linked to CLO-3, revisited explicitly in Session 24 and 30).

## 13. Suggested homework

- Convert one of your session-2 exercises into a clean, documented notebook following the checklist.
- Practice markdown: format your session-3 notebook with headings, a numbered list, and a bold key finding.
- Read: Jupyter notebook docs section "User interface" (skim).
- Watch (optional): any 5-minute video on Jupyter keyboard shortcuts — learn 3 new ones.