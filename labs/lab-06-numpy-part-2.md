# Lab 06 — NumPy II: Masks, Aggregation, Random, Broadcasting

**Session:** Week 3 · Session 6 · 90 min
**CLO:** CLO-1
**Difficulty:** Beginner

## Learning objectives

By the end of this lab you can:

1. Filter arrays with boolean masks and combine conditions with `&`, `|`, `~`.
2. Aggregate with `min`, `max`, `mean`, `std`, `percentile`.
3. Generate reproducible random data and sample from it.
4. Use broadcasting rules to avoid explicit loops.

## Problem statement

A weather station records hourly temperatures for a month (30 days × 24
hours). A single NumPy array must answer: which days froze (any hour below
0 °C), the warmest hour of the month, the 10th percentile temperature, and
a simulated "sensor noise" addition — all without a single Python loop.

## Dataset requirements

Synthetic, generated inline with `np.random` and a fixed seed.

## Step-by-step tasks

1. **Generate:** `np.random.seed(11)`; build
   `temps = np.random.normal(loc=15, scale=8, size=(30, 24))` and clip to a
   plausible range with `np.clip(temps, -5, 40)`. Print shape.
2. **Mask:** build `froze = temps.min(axis=1) < 0` — a boolean per day.
   Print `np.sum(froze)` (days that froze) and the indices with
   `np.argwhere(froze).ravel()`.
3. **Filter:** print the actual minimum temperature(s) of any freezing day
   using `temps[froze].min()`.
4. **Aggregate:** report month `min`, `max`, `mean`, `std`, and the 10th and
   90th percentiles via `np.percentile`.
5. **Warmest hour:** use `np.unravel_index(temps.argmax(), temps.shape)` to
   get (day, hour). Explain what `unravel_index` does in a comment.
6. **Broadcasting:** normalize the array with
   `normalized = (temps - temps.mean(axis=0)) / temps.std(axis=0)` — no
   loop, and both operands broadcast. Verify `normalized.mean()` is ~0 and
   `normalized.std()` is ~1 (allow rounding).
7. **Noise simulation:** add `np.random.normal(0, 0.5, temps.shape)` noise
   to a copy — same shape, element-wise — and confirm the copy differs from
   the original by more than `0` somewhere.

## Starter code

```python
import numpy as np

np.random.seed(11)
temps = np.random.normal(loc=15, scale=8, size=(30, 24))
temps = np.clip(temps, -5, 40)

print("shape:", temps.shape)
# your code here for tasks 2-7
```

## Expected output

- `shape: (30, 24)`
- `froze` has some `True` values; `np.sum(froze)` printed.
- A single scalar for the coldest freezing hour.
- Four aggregation scalars + two percentiles.
- A `(day, hour)` tuple for the warmest hour.
- `normalized.mean()` ≈ 0.0 and `normalized.std()` ≈ 1.0.
- A `True` for "noisy copy differs".

## Questions

1. Why does `temps[froze]` flatten to 1-D? What shape did you expect?
2. When would you use `np.percentile` instead of `mean`?
3. In step 6, what shapes are `temps.mean(axis=0)` and `temps.std(axis=0)`?
   How does broadcasting align them with `(30, 24)`?
4. Why is `&` used instead of `and` in NumPy masks?
5. What does `np.unravel_index` convert, and why is it needed?

## Challenge task

Find the **longest streak** of consecutive hours with temperature above
25 °C anywhere in the month (flatten the array first). Hint: build a
boolean array, then use `np.diff` on the indices where the condition is
`True`. Print the streak length and the (day, hour) where it starts.
Comment your approach.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Data generated + clipped + shape | 2 | (30, 24) |
| Freeze mask + counts + indices | 3 | boolean logic correct |
| Filtered min on freezing days | 2 | uses mask |
| Aggregations + percentiles | 3 | values match seed |
| `unravel_index` used & explained | 3 | correct (day, hour) |
| Broadcasting normalization | 3 | mean≈0, std≈1 |
| Noise addition on a copy | 2 | differs from original |
| Answers to questions | 2 | Q1, Q4 correct |
| Challenge: longest streak | 4 | correct length + start |
| **Total** | **24** | |