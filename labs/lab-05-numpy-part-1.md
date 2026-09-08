# Lab 05 — NumPy I: Arrays, Creation, Indexing, dtypes

**Session:** Week 3 · Session 5 · 90 min
**CLO:** CLO-1
**Difficulty:** Beginner

## Learning objectives

By the end of this lab you can:

1. Create `ndarray`s with `np.array`, `np.arange`, `np.zeros`, `np.ones`,
   `np.linspace`, `np.full`.
2. Inspect `shape`, `ndim`, `dtype`, and `size`.
3. Index and slice 1-D and 2-D arrays (rows, columns, steps).
4. Explain why arrays are faster than lists and why a single dtype matters.

## Problem statement

A retail chain records daily footfall (visitors per hour) across three
stores for one day: 24 hourly readings per store, stored as a 2-D array of
shape `(3, 24)`. Using only NumPy, you must: build the array, pull specific
hours, compute per-store and per-hour summaries, and prove you can slice
without copying mistakes.

## Dataset requirements

Generate the data inline with `np.random` using a fixed seed, so every run
is identical. No files.

## Step-by-step tasks

1. **Generate** the array: `np.random.seed(7)`, then
   `footfall = np.random.randint(0, 60, size=(3, 24))`. Print shape, ndim,
   dtype, size — explain each in a comment.
2. **Slice the morning** (hours 8–11, columns 8:12) for all stores. Print it.
3. **Extract Store 2's entire day** (row index 1). What is its shape after
   slicing — and why is it not `(1, 24)`? Fix it with `reshape(1, -1)` and
   compare.
4. **Per-store totals** with `sum(axis=1)` — write in a comment which axis
   sums away and why.
5. **Per-hour mean** across stores with `mean(axis=0)`.
6. **Busiest hour:** find the hour (column) with the highest total across
   stores using `argmax` on the column sums.
7. **Convert** the array to `float64`, add 0.5, and confirm the dtype
   changed. Explain why mixed types in one array are impossible.

## Starter code

```python
import numpy as np

np.random.seed(7)
footfall = np.random.randint(0, 60, size=(3, 24))

print("shape:", footfall.shape)
print("ndim:", footfall.ndim)
print("dtype:", footfall.dtype)
print("size:", footfall.size)

# your code here for tasks 2-7
```

## Expected output

- `shape: (3, 24)`, `ndim: 2`, `dtype: int64`, `size: 72`.
- Morning slice: a `(3, 4)` block of integers.
- Store 2's day: a 1-D array of 24 ints; after reshape `(1, 24)`.
- Per-store totals: three numbers summing to the same as `footfall.sum()`.
- Per-hour means: 24 floats.
- Busiest hour: an integer hour index (0–23) — with a fixed seed this is
  deterministic; your answer must match `np.argmax(footfall.sum(axis=0))`.

## Questions

1. What does `axis=0` mean in `sum(axis=0)`? `axis=1`?
2. Why does slicing a single row give a 1-D array? How do you keep it 2-D?
3. What is `dtype`, and why must all elements share one?
4. `footfall[1, 8:12]` vs `footfall[1][8:12]` — same result? Explain.
5. Why use `np.random.seed(7)` in a lab?

## Challenge task

Create a **masked comparison** without `where`: produce a boolean array
`busy = footfall > 40`, count how many hours each store was "busy"
(`busy.sum(axis=1)`), and report which store had the most busy hours.
Then explain in one comment why `busy` is `bool` dtype and what that means
for `sum`.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Array created + attributes explained | 3 | shape/ndim/dtype/size correct |
| Morning slice correct | 2 | `(3, 4)` block |
| Row slice + reshape reasoning | 3 | shape explained, reshape used |
| Axis sums correct & commented | 3 | totals match `footfall.sum()` |
| Hour mean + busiest hour via argmax | 3 | matches seeded expectation |
| dtype conversion task | 2 | float64 confirmed |
| Answers to questions | 2 | Q1, Q4 correct |
| Challenge: busy-hours mask | 3 | boolean mask + counts + store id |
| **Total** | **21** | |