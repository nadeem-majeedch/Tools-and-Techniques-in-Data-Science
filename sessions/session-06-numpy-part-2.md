# Session 6 — NumPy II: Operations, Broadcasting, Random

**Week 3 · Session 6 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Apply element-wise operations (arithmetic, comparisons, ufuncs) to arrays.
- Use boolean masks to filter and count array elements.
- Explain broadcasting rules at a practical level and use them safely.
- Aggregate arrays with `sum`, `mean`, `min`, `max`, `std`, and `axis`-wise variants.
- Generate reproducible random arrays with `np.random` and a fixed seed.

## 2. Key concepts

- **Universal functions (ufuncs)** — element-wise math on whole arrays (`np.sqrt`, `np.exp`, comparisons…).
- **Boolean masks** — `arr[arr > 5]` filters; masks are the workhorse of data selection.
- **Broadcasting** — NumPy stretches a smaller array to match a bigger one without copying.
- **Aggregation with `axis`** — collapse along rows (`axis=0`) or columns (`axis=1`).
- **Randomness with a seed** — reproducibility: same seed → same numbers, every run.
- Real data pipelines are: load → filter → aggregate. This session builds those verbs.

## 3. Detailed lecture notes

**Why this session?** Session 5 gave you the container; today you learn the
operations that make it useful — the verbs of data work: transform, filter,
summarize. Every later Pandas operation (`df["col"].mean()`, boolean filters)
maps directly to a NumPy operation you'll learn today.

**Ufuncs and element-wise math.** `a + 1`, `a * 2`, `a ** 2`, `np.sqrt(a)`,
`np.log(a)`, `np.abs(a)`, and comparisons `a > 5` all apply element-wise, in C
speed. This is vectorization in practice. Show the loop vs. vectorized comparison
once more with `%timeit` — the lesson sticks when students *see* it.

**Boolean masks.** `a > 5` yields an array of True/False. Use it directly:
`a[a > 5]` returns only the True positions. Count with `(a > 5).sum()`, get the
mean of a subset with `a[a > 5].mean()`. Combine conditions with `&` (and),
`|` (or), `~` (not) — note the difference from Python's `and`/`or` (those don't
work on arrays; they evaluate truthiness). This pattern — filter, then summarize
— is the single most repeated move in data science.

**Broadcasting.** Explain with a story: "adding a column vector to a matrix".
NumPy aligns dimensions from the right and stretches size-1 dimensions. Practical
rules: shapes `(3,1)` + `(3,)` works because `(3,)` becomes `(1,3)`… no — careful.
The rule: broadcastable if dimensions are equal **or** one of them is 1,
compared right-to-left. Examples: `(2,3) + (3,)` → `(3,)` becomes `(1,3)` →
works. `(2,3) + (2,)` → `(2,)` vs `(3,)` mismatch → error. Keep it concrete:
standardize a column: `(temps - temps.mean(axis=0)) / temps.std(axis=0)` — this
is z-scoring, and it works because `temps.mean(axis=0)` has shape `(3,)` and
broadcasts across rows. That's the real payoff: **row-wise statistics applied to
every row without a loop.**

**Aggregation and axis.** `arr.mean()`, `arr.sum()`, `arr.std()`, `arr.min()`,
`arr.max()` collapse everything to a scalar. With `axis=0` you collapse rows
→ one value per column; with `axis=1` you collapse columns → one value per row.
Memory hook: axis 0 is "down the rows", axis 1 is "across the columns"; the
result's shape is the *other* dimension.

**Random numbers.** `np.random.seed(42)` before generating ensures the same
numbers every run — the foundation of reproducible experiments (your model
results must be repeatable!). `np.random.rand(3, 4)` uniform [0,1),
`np.random.randint(0, 100, 10)` integers, `np.random.normal(0, 1, 1000)` normal.
"Random" without a seed is fine for games; in data science you want to be able
to re-run. This is a habit the rubric checks.

## 4. Important terminology

- **Ufunc** — vectorized element-wise function (`np.sqrt`, `np.exp`, `+`, `>`).
- **Boolean mask** — an array of True/False used for selection.
- **Broadcasting** — implicit shape-stretching so arrays of different shapes combine.
- **Axis** — direction of aggregation: `axis=0` rows, `axis=1` columns.
- **Aggregation** — reducing many values to one (`mean`, `sum`, `std`).
- **Seed** — the starting point of a pseudo-random sequence; same seed → same sequence.
- **Vectorized operation** — an operation applied to all elements at once.
- **Z-score** — `(x - mean) / std`, a standard normalization.

## 5. Python examples

```python
import numpy as np
np.random.seed(42)                     # reproducible randomness

arr = np.random.randint(1, 101, 12).reshape(3, 4)
print(arr)

# --- Ufuncs ---
print(np.sqrt(arr[:3]))                # element-wise sqrt of first 3 elements
print((arr + 1) * 2)

# --- Boolean masks ---
big = arr[arr > 50]
print("Count above 50:", big.size)
print("Mean above 50:", big.mean())

# --- Broadcasting: z-score each column ---
col_mean = arr.mean(axis=0)            # shape (4,)
col_std = arr.std(axis=0)
z = (arr - col_mean) / col_std         # (3,4) - (4,) -> broadcast
print("Each column now has mean ~0:", np.round(z.mean(axis=0), 10))

# --- Axis aggregation ---
print("Row sums:", arr.sum(axis=1))    # one value per row
print("Column maxes:", arr.max(axis=0))# one value per column
```

## 6. Beginner example

```python
import numpy as np

heights = np.array([1.55, 1.70, 1.62, 1.80, 1.68])   # meters
print("Taller than 1.65:", heights[heights > 1.65])
print("Average height:", round(heights.mean(), 2))
```

Filter + aggregate in two lines — the pattern of the day.

## 7. Practical Data Science example

```python
import numpy as np
np.random.seed(7)

# Simulate 30 days of customer counts (a stand-in for a real dataset)
daily_customers = np.random.poisson(lam=120, size=30)

# --- Analysis questions a manager would ask ---
print("Total customers (month):", daily_customers.sum())
print("Average per day:", round(daily_customers.mean(), 1))
print("Busiest day:", daily_customers.max())
print("Quiet days (<100):", (daily_customers < 100).sum())

# --- Standardize for comparison with another branch ---
mean, std = daily_customers.mean(), daily_customers.std()
z = (daily_customers - mean) / std
print("First z-score:", round(z[0], 2), "(units = standard deviations from the mean)")

# --- Reproducibility: rerun with same seed, get identical numbers ---
np.random.seed(7)
again = np.random.poisson(lam=120, size=30)
print("Identical on rerun:", (again == daily_customers).all())
```

## 8. In-class activity (50 min)

Continue in `notebooks/week-03/session-06-numpy-2.ipynb`:

1. **Warm-up (10 min):** create `np.random.seed(0)`; `arr = np.random.randint(0, 100, 24).reshape(6, 4)`. Print shape and dtypes.
2. **Filter drills (15 min):** (a) count values ≥ 50; (b) mean of values in the last column; (c) count values between 20 and 80 (`&`); (d) replace all values > 90 with 90 (clipping).
3. **Axis challenge (10 min):** compute row means and column sums; verify one by hand.
4. **Broadcasting puzzle (15 min):** z-score each column and each row; explain in markdown why both work. Predict which of `(6,4)+(6,)` and `(6,4)+(4,)` works before running.

## 9. Lab exercise

**Lab 1 is due today** (push before session end if possible, otherwise before
tomorrow's deadline): `labs/lab-01/` — NumPy arrays, operations, masks,
aggregation, plus checkpoint questions. Graded per `../assessment-plan.md`.

## 10. Common mistakes

- Using `and`/`or` instead of `&`/`|` in masks → "truth value of an array is ambiguous".
- Forgetting parentheses: `arr[(arr > 20) & (arr < 80)]` — `&` binds tighter than comparisons.
- Setting a seed *inside* a loop → same "random" values each iteration.
- Wrong axis: `arr.mean(axis=0)` when they wanted row means.
- Expecting `arr[arr > 5]` to keep 2-D shape — it flattens to 1-D (that's normal).
- Broadcasting errors: mixing shapes `(2,3)` and `(2,)` → understand the error before guessing.

## 11. Short assessment questions

1. `a = np.array([3, 8, 1])` — what does `a[a > 3]` return?
2. What is the result of `(a > 3).sum()` for that array?
3. What does `arr.mean(axis=1)` compute?
4. Why do we set `np.random.seed(...)` in data science code?
5. Which of these broadcasts fine: `(2,3) + (3,)` or `(2,3) + (2,)`? Why?
6. `np.sqrt(a)` — element-wise or dot product? (Element-wise.)

## 12. CLO mapping

CLO-1: filtering, aggregation, and normalization are core manipulation skills for
datasets. The mask pattern transfers directly to Pandas (Sessions 7–10), and
z-scoring reappears in ML preprocessing (Sessions 21–22).

## 13. Suggested homework

- Read: NumPy quickstart sections 5–6 (operations, broadcasting) — skim, don't memorize.
- Practice: generate `np.random.normal(170, 10, 1000)` (heights in cm); compute mean, std, and the share of values within ±1 std. Note the result (~68%) — statistics is coming in Session 15.
- Preview: `import pandas as pd; s = pd.Series([1,2,3]); print(s)` — Session 7 explains what a Series is and why it's more than an array.