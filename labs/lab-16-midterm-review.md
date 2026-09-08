# Lab 16 — Midterm Review: Cumulative Practical

**Session:** Week 8 · Session 16 · 90 min
**CLO:** CLO-1
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Combine every Module A skill under time pressure.
2. Read a task spec and translate it into pandas/NumPy/viz code.
3. Self-check your output against stated expectations.
4. Work in a clean, restart-safe notebook (as in the exam).

## Problem statement

This is a **mock exam**: a fresh dataset, a written spec, a time box. You
get 70 minutes and one notebook. The tasks deliberately mirror the real
midterm's shape — cleaning, computation, a plot, and written answers. Do
**not** consult prior labs; rely on what you can recall and verify by
running code.

## Dataset requirements

Seaborn built-in `flights` (144 rows: year × month passenger counts).
No cleaning files — everything inline.

## Step-by-step tasks (complete in order)

1. **Load & shape:** load flights, print `shape`, `info()`, `head()`.
   (2 min)
2. **Clean:** convert `month` to title case (strip + capitalize), confirm
   with `value_counts()`. Confirm no missing values. (5 min)
3. **Numeric:** compute with NumPy: mean, std, min, max of `passengers`,
   plus the 25th and 75th percentiles via `np.percentile`. (5 min)
4. **Aggregate:** the year with the most total passengers
   (`groupby("year")["passengers"].sum().idxmax()`), and the busiest
   single month overall (`idxmax` on passengers). (5 min)
5. **Filter + sort:** show the 5 rows with the most passengers, sorted
   descending; then rows where `passengers > 500` — how many? (8 min)
6. **Plot:** one line plot of passengers over time (use
   `pd.to_datetime` on `year`+`month` first, or plot by year with month
   as hue) with labeled axes and title. Save to
   `datasets/flights-trend.png`. (10 min)
7. **Written answers (in markdown):**
   a. Which decade shows the fastest growth, and what evidence supports it?
   b. Why must `month` be normalized before grouping?
   c. Give one reason the plot would mislead if months were out of order.
   (15 min)
8. **Hygiene:** Restart & Run All; every cell must pass. (10 min)
9. **Self-check:** compare your outputs against the expected output table
   below and note any mismatch in one sentence. (10 min)

## Starter code

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

flights = sns.load_dataset("flights")
# your code here — tasks 1-8
```

## Expected output

- `shape: (144, 3)`, no nulls.
- `month` normalized: 12 distinct values, title case.
- passengers: min 104, max 622, mean ≈ 280.3, std ≈ 119.0 (approx);
  percentiles: 25% ≈ 180, 75% ≈ 360 (values rounded; match your own
  computation).
- Busiest year: 1960. Busiest month overall: July 1960.
- Rows with `passengers > 500`: 8.
- Plot saved; trend visibly rising 1958–1960.

## Questions

1. Why would `flights["month"].str.capitalize()` alone be insufficient if
   the data had leading spaces? (Hint: strip first.)
2. `idxmax()` returns an index label — what is it for the busiest year?
3. Why is a line plot better than a bar plot for a time series?
4. What does `np.percentile(passengers, [25, 75])` return — one number or
   two?
5. During the exam, a cell errors with a `KeyError: 'month'`. List two
   likely causes you would check first.

## Challenge task

In the remaining time, build a **pivot table**:
`flights.pivot(index="year", columns="month", values="passengers")` and
confirm `pivot` is the right tool here (vs. `pivot_table` — why no
aggregation needed?). Then answer: which year had the highest *September*
traffic? (Use `.loc` on the pivot.)

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Load + shape + info | 3 | (144, 3) |
| Month normalization | 3 | title case, 12 values |
| NumPy summary stats | 4 | min/max/mean/std/percentiles |
| Aggregations (year, month) | 4 | 1960 + July 1960 |
| Filter/sort counts | 3 | 5 rows, 8 rows >500 |
| Plot + save | 4 | labeled, file exists |
| Written answers | 4 | a–c addressed |
| Restart-safe notebook | 3 | runs top-to-bottom |
| Self-check note | 2 | mismatch documented |
| Challenge: pivot | 4 | pivot used, September answer |
| **Total** | **34** | |