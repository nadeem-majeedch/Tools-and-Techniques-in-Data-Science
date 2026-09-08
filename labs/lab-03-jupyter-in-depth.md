# Lab 03 — Jupyter in Depth

**Session:** Week 2 · Session 3 · 90 min
**CLO:** CLO-1
**Difficulty:** Beginner

## Learning objectives

By the end of this lab you can:

1. Use markdown cells with headings, lists, tables, and code formatting.
2. Use magic commands (`%timeit`, `%matplotlib inline`, `%%time`).
3. Explain what a kernel is and restart/clear outputs safely.
4. Keep a notebook clean: run top-to-bottom, no hidden state.

## Problem statement

A messy notebook is a liability: a cell that "worked earlier" fails after a
restart because it depended on hidden state. You will build a **clean,
restart-safe** notebook that analyzes a small dataset, and you will prove
its cleanliness by restarting the kernel and running all cells in order.

## Dataset requirements

Seaborn's built-in `tips` dataset (244 rows). Load it with
`sns.load_dataset("tips")` — no download needed.

## Step-by-step tasks

1. **Title + intro cell:** a markdown cell with a `#` heading, a one-line
   description, and your name/date.
2. **Imports cell:** put ALL imports in the first code cell.
3. **Data load cell:** load tips and print `shape` and `head()`.
4. **Analysis cell:** compute the mean tip by day using `groupby`, show it
   as a markdown table in the NEXT (markdown) cell.
5. **Speed cell:** time a cell that computes `df["tip"].mean()` with
   `%timeit` — write down the number in markdown.
6. **Prove restart-safety:** use the Jupyter menu *Kernel → Restart & Run
   All*. Every cell must run top-to-bottom with no errors.
7. **Trap check:** write a code cell that uses a variable `secret` which is
   NOT defined in any earlier cell. Restart & Run All — the cell must fail.
   Fix the notebook by defining `secret` properly, then re-run cleanly.
8. **Hygiene pass:** clear all outputs (Edit → Clear All Outputs), then
   Restart & Run All one final time.

## Starter code

```python
# Cell 1 — imports (everything in one place)
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
```

```python
# Cell 2 — load data
tips = sns.load_dataset("tips")
print("shape:", tips.shape)
tips.head()
```

```python
# Cell 3 — analysis
mean_tip_by_day = tips.groupby("day")["tip"].mean().round(2)
mean_tip_by_day
```

```python
# Cell 4 — timing
%timeit tips["tip"].mean()
```

```python
# Cell 5 — the trap (intentionally broken at first)
print(secret)
```

## Expected output

- Cell 2: `shape: (244, 7)` plus the first 5 rows.
- Cell 3: a Series with mean tips per day (`Fri 2.73, Sat 2.99, Sun 3.26,
  Thur 2.77` approximately).
- Cell 4: a `%timeit` result like `12.1 µs ± ... per loop`.
- Cell 5: `NameError: name 'secret' is not defined` **until you fix it**;
  after the fix it prints whatever value you assigned.
- Final run: **zero errors** from top to bottom.

## Questions

1. What is a kernel, and what does "restart" actually reset?
2. Why does the order of cells matter even though Jupyter lets you run them
   in any order?
3. What does `%timeit` do differently from `%%time`?
4. Your notebook runs fine, but a classmate's copy errors with `NameError`.
   What is the most likely cause?
5. Why should imports live in the first cell?

## Challenge task

Add a markdown "report" cell at the end that summarizes the tips dataset in
exactly three sentences: one about size, one about the day with the highest
mean tip, and one about the range of `total_bill`. Format the three
sentences as a bulleted list, and bold the day name. Keep it restart-safe.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Title/intro markdown cell | 2 | heading, description, name/date |
| Imports in one first cell | 2 | verified in final run |
| Data load + shape output | 2 | `(244, 7)` |
| Groupby analysis + markdown table | 3 | numbers match |
| `%timeit` result recorded | 2 | value in markdown |
| Trap cell fixed properly | 3 | defined before use, not deleted |
| Final Restart & Run All clean | 3 | no errors |
| Challenge: 3-sentence report | 3 | bullets, bolded day, restart-safe |
| **Total** | **20** | |