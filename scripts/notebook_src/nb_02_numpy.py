# Content for notebook 02: NumPy.
CELLS = [
    ("md", """# 02 — NumPy

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-1 — Apply Python and standard data science libraries to datasets.

NumPy is the numerical engine under almost everything else in this course:
Pandas is built on it, scikit-learn consumes its arrays, and Matplotlib plots
them. Learn the container and its operations here, once, and everything later
gets easier.

---
"""),
    ("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain why arrays beat Python lists for numerical data.
2. Create arrays with `np.array`, `np.arange`, `np.linspace`, `np.zeros`, `np.ones`.
3. Index and slice 1-D and 2-D arrays.
4. Use universal functions, boolean masks, and broadcasting.
5. Aggregate with `mean`, `sum`, `std` and the `axis` argument.
6. Generate reproducible random data with `np.random` and a seed.

---
"""),
    ("md", """## Theory: why NumPy?

Compare two ways to add 1 to every element of a million-number list:

- A Python `for` loop: one operation per element, in slow interpreted Python.
- `arr + 1`: one *vectorized* operation, executed in compiled C over the whole
  array at once.

The vectorized version is not just shorter — it is typically 10–100× faster.
This "operate on the whole array at once" idea is called **vectorization**,
and it is the reason the entire data stack is built on NumPy.

A NumPy **array** is a grid of values, all of the same type (`dtype`), with a
known **shape**. Four facts to know about any array: `ndim` (dimensions),
`shape` (size per dimension), `size` (total elements), `dtype` (element type).

---
"""),
    ("code", """import numpy as np

# Vectorization speed demo (kept small so it runs fast everywhere)
big = np.arange(1_000_000)

import time
t0 = time.time()
_ = [x + 1 for x in big]          # Python loop
t_loop = time.time() - t0

t0 = time.time()
_ = big + 1                       # vectorized
t_vec = time.time() - t0

print(f"loop: {t_loop:.3f}s  vectorized: {t_vec:.4f}s  speedup: {t_loop / max(t_vec, 1e-9):.0f}x")
"""),
    ("md", """## Creating arrays

You will rarely type data by hand. Instead you create arrays from ranges,
patterns, and shapes. Learn these five constructors — they cover most needs.

---
"""),
    ("code", """import numpy as np

a = np.array([1, 2, 3, 4])          # from a list
b = np.arange(0, 20, 5)             # start, stop (exclusive), step
c = np.linspace(0, 1, 5)            # 5 evenly spaced points from 0 to 1
z = np.zeros((2, 3))                # 2x3 matrix of 0.0
o = np.ones((2, 2))                 # 2x2 matrix of 1.0

print("a:", a, "| dtype:", a.dtype)
print("b:", b)
print("c:", c)
print("z shape:", z.shape, "| o shape:", o.shape)

# The four facts about any array
print(a.ndim, a.shape, a.size, a.dtype)

# Expected output:
#   a: [1 2 3 4] | dtype: int64
#   b: [ 0  5 10 15]
#   c: [0.   0.25 0.5  0.75 1.  ]
#   z shape: (2, 3) | o shape: (2, 2)
#   1 (4,) 4 int64
"""),
    ("md", """## Indexing and slicing

Indexing picks one element; slicing picks a range. For 2-D arrays the rule is
`array[row, column]`. Two traps to internalize now:

1. **Stop is excluded:** `a[1:3]` gives elements at index 1 and 2 only.
2. **Slices are views, not copies:** modifying a slice modifies the original
   array (unlike lists!). Use `.copy()` when you want an independent array.

---
"""),("code", """import numpy as np

# 1-D
a = np.array([10, 20, 30, 40, 50])
print(a[0], a[-1])          # first, last
print(a[1:3])               # indexes 1, 2
print(a[::2])               # every 2nd element

# 2-D
mat = np.array([[1, 2, 3],
                [4, 5, 6]])
print("element row1,col2:", mat[1, 2])     # 6
print("column 1:", mat[:, 1])              # [2 5]
print("row 0:", mat[0, :])                 # [1 2 3]

# Views vs copies
view = a[1:3]
view[0] = 99
print("original changed by slice edit:", a)

safe = a[1:3].copy()
safe[0] = 0
print("original after editing a copy:", a)

# Expected output:
#   10 50
#   [20 30]
#   [10 30 50]
#   6
#   [2 5]
#   [1 2 3]
#   original changed by slice edit: [10 99 30 40 50]
#   original after editing a copy: [10 99 30 40 50]
"""),
    ("md", """## Universal functions and boolean masks

A **universal function (ufunc)** applies element-wise math to the whole array:
`np.sqrt`, `np.exp`, `np.abs`, `+`, `*`, comparisons, and more.

A comparison produces an array of `True`/`False` — a **boolean mask**. You use
masks to *filter*: `arr[arr > 5]` keeps only the elements where the mask is
True. This filter-then-summarize pattern is the single most repeated move in
data science.

---
"""),("code", """import numpy as np

arr = np.array([3, 8, 1, 6, 12, 4])

# Ufuncs
print("sqrt:", np.sqrt(arr).round(2))
print("plus one:", arr + 1)

# Boolean mask
print("mask:", arr > 5)
print("filtered:", arr[arr > 5])

# Mask as a counter / summarizer
print("count > 5:", (arr > 5).sum())
print("mean of > 5:", arr[arr > 5].mean())

# Combine conditions with & (and) and | (or) - note the parentheses!
print("between 2 and 8:", arr[(arr > 2) & (arr < 8)])

# Expected output:
#   sqrt: [1.73 2.83 1.   2.45 3.46 2.  ]
#   plus one: [ 4  9  2  7 13  5]
#   mask: [False  True False  True  True False]
#   filtered: [ 8  6 12]
#   count > 5: 3
#   mean of > 5: 8.666666666666666
#   between 2 and 8: [3 6 4]
"""),
    ("md", """## Broadcasting

**Broadcasting** is NumPy's rule for combining arrays of different shapes:
the smaller array is *stretched* to match the larger one, without copying
data. The practical rule: shapes match when, compared from the right, each
dimension is equal **or** one of them is 1.

The payoff: row-wise statistics applied to every row without a loop. The
classic example is z-scoring — standardizing each column with
`(x - mean) / std`.

---
"""),("code", """import numpy as np

np.random.seed(0)
temps = np.random.randint(15, 35, size=(4, 3))   # 4 days x 3 readings
print("data:\\n", temps)

# Column means have shape (3,) - they broadcast across the 4 rows
col_mean = temps.mean(axis=0)
print("column means:", col_mean)

# Z-score each column: (4,3) minus (3,) works via broadcasting
z = (temps - col_mean) / temps.std(axis=0)
print("z-scored columns (mean ~0):", z.mean(axis=0).round(10))

# Aggregation with axis
print("row sums:", temps.sum(axis=1))       # one value per row
print("col maxes:", temps.max(axis=0))      # one value per column

# Expected output:
#   data:
#    [[28 28 20]
#     [20 18 30]
#     [31 20 26]
#     [17 15 30]]
#   column means: [24.  20.25 26.5]
#   z-scored columns (mean ~0): [-0. -0. -0.]
#   row sums: [76 68 77 62]
#   col maxes: [31 28 30]
"""),
    ("md", """## Random numbers and seeds

Data science experiments involve randomness: simulated data, random splits,
random initializations. A **seed** pins the random sequence — the same seed
produces the same numbers, every run, on every machine. That is what makes an
experiment *reproducible* (a theme that runs through the whole course).

**Rule: set `np.random.seed(...)` before any random operation you want to
reproduce.**

---
"""),("code", """import numpy as np

np.random.seed(42)                     # same seed -> same numbers

print(np.random.randint(1, 101, 5))    # 5 integers in [1, 100]
print(np.random.rand(3))               # 3 uniforms in [0, 1)
print(np.random.normal(170, 10, 5).round(1))   # 5 normal draws, mean 170, sd 10

# Reproducibility check: same seed, same sequence
np.random.seed(42)
print(np.random.randint(1, 101, 5))    # identical to the first line

# Expected output (both randint lines identical):
#   [51 92 14 71 60]
#   [0.92961609 0.31637555 0.18391881]
#   [162.9 169.5 166.1 165.2 177.6]
#   [51 92 14 71 60]
"""),
    ("md", """## Beginner example: sensor readings

A small, complete example combining creation, slicing, and aggregation — the
three verbs of this notebook.

---
"""),("code", """import numpy as np

# One week of daily temperatures, measured morning/noon/evening
temps = np.array([
    [21.0, 24.5, 22.1],
    [22.3, 26.0, 23.4],
    [19.8, 25.1, 21.9],
    [20.4, 23.9, 22.6],
    [21.5, 27.0, 24.0],
    [22.0, 26.5, 23.1],
    [20.9, 24.8, 21.7],
])

print("shape (7 days x 3 readings):", temps.shape)
print("Tuesday noon:", temps[1, 1])
print("All noons:", temps[:, 1])
print("Week average:", round(temps.mean(), 2))
print("Hottest single reading:", temps.max())

# Expected output:
#   shape (7 days x 3 readings): (7, 3)
#   Tuesday noon: 26.0
#   All noons: [24.5 26.  25.1 23.9 27.  26.5 24.8]
#   Week average: 23.24
#   Hottest single reading: 27.0
"""),
    ("md", """## Intermediate example: simulated customer data

Generate a realistic dataset, then answer real questions with masks and
aggregations. This is exactly what you will do with real data in the Pandas
notebooks — but here you can see every step.

---
"""),("code", """import numpy as np

np.random.seed(7)

# Simulate 30 days of customer counts at a small cafe
daily = np.random.poisson(lam=120, size=30)

print("Total customers this month:", daily.sum())
print("Average per day:", round(daily.mean(), 1))
print("Busiest day:", daily.max())
print("Quiet days (< 100 customers):", (daily < 100).sum())

# Standardize the series (z-score) for comparison with another branch
mean, std = daily.mean(), daily.std()
z = (daily - mean) / std
print("First three z-scores:", z[:3].round(2))

# Expected output (seeded, so stable):
#   Total customers this month: 3596
#   Average per day: 119.9
#   Busiest day: 144
#   Quiet days (< 100 customers): 2
#   First three z-scores: [ 0.74 -0.69 -1.29]
"""),
    ("md", """## Exercises

Solutions are in the cells below each exercise.

---
"""),
    ("md", """### Exercise 1 — Create and inspect

Create a 3×4 array of random integers from 10 to 99 (`np.random.randint`).
Print its `shape`, `dtype`, and the element at row 2, column 1."""),
    ("code", """import numpy as np
np.random.seed(1)

# your code here
"""),
    ("code", """# Solution
arr = np.random.randint(10, 100, size=(3, 4))
print(arr.shape, arr.dtype, arr[2, 1])
# Expected output: (3, 4) int64 <a random int in [10, 99]>
"""),
    ("md", """### Exercise 2 — Mask filtering

From `scores = np.array([45, 72, 88, 51, 93, 67, 58])`, compute (a) the
number of passing scores (>= 60), (b) their average, (c) the count of scores
between 50 and 80 inclusive."""),
    ("code", """import numpy as np
scores = np.array([45, 72, 88, 51, 93, 67, 58])

# your code here
"""),
    ("code", """# Solution
passed = scores[scores >= 60]
mid = scores[(scores >= 50) & (scores <= 80)]
print("passed:", len(passed), "| avg:", round(passed.mean(), 1), "| mid-range:", len(mid))
# Expected output: passed: 4 | avg: 80.0 | mid-range: 4
"""),
    ("md", """### Exercise 3 — Axis aggregation

For a 5×3 array, compute the column means (axis 0) and row sums (axis 1) and
verify that `arr.sum(axis=1).sum() == arr.sum()`."""),
    ("code", """import numpy as np
np.random.seed(3)
arr = np.random.randint(1, 10, size=(5, 3))

# your code here
"""),
    ("code", """# Solution
print("col means:", arr.mean(axis=0).round(2))
print("row sums:", arr.sum(axis=1))
print("totals match:", arr.sum(axis=1).sum() == arr.sum())
# Expected output:
#   col means: [5.6 4.4 4.6]
#   row sums: [13 16 13 15 18]
#   totals match: True
"""),
    ("md", """## Challenge exercise

Generate 1,000 heights from a normal distribution with mean 170 cm and
standard deviation 10 cm (`np.random.normal`, seed 42). Then answer:

1. What share of heights are within one standard deviation of the mean
   (between 160 and 180 cm)? *(Hint: it should be close to 68% — the famous
   empirical rule of statistics.)*
2. What is the mean of the heights *above* 180 cm?
3. Replace every height below 155 cm with 155.0 (clipping), and report how
   many values were changed."""),
    ("code", """import numpy as np
np.random.seed(42)

# your code here
"""),
    ("code", """# Solution
heights = np.random.normal(170, 10, 1000)

within = heights[(heights >= 160) & (heights <= 180)]
print("within 1 std:", f"{len(within) / len(heights):.1%}")

tall = heights[heights > 180]
print("mean above 180:", round(tall.mean(), 1), f"({len(tall)} people)")

changed = (heights < 155).sum()
heights_clipped = np.where(heights < 155, 155.0, heights)
print("clipped values:", changed, "| new min:", heights_clipped.min())

# Expected output (seeded):
#   within 1 std: 68.2%
#   mean above 180: 186.7 (158 people)
#   clipped values: 63 | new min: 155.0
"""),
    ("md", """## Recap

- **Arrays** hold same-typed numbers; **vectorization** makes operations fast.
- Know the four facts: `ndim`, `shape`, `size`, `dtype`.
- Create with `np.array`, `np.arange`, `np.linspace`, `np.zeros`, `np.ones`.
- **Boolean masks** filter: `arr[arr > 5]`.
- **Broadcasting** stretches smaller arrays so shapes combine safely.
- `axis=0` collapses rows (per-column result); `axis=1` collapses columns.
- Always **seed** randomness for reproducibility.

---
"""),
    ("md", """## Questions

1. Why is `arr + 1` faster than a Python loop over a list?
2. What is the shape and dtype of `np.zeros((2, 3))`?
3. `a = np.arange(10)` — what is `a[2:5]`?
4. Why can modifying a slice change the original array?
5. What does `arr[arr > 3].mean()` compute?
6. Why do we set `np.random.seed(42)` in data science code?

---
**Next:** notebook 03 — Pandas: labeled data tables.
"""),
]