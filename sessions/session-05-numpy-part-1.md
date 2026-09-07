# Session 5 — NumPy I: Arrays

**Week 3 · Session 5 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Explain why arrays beat Python lists for numerical data.
- Create `ndarray`s from lists, `np.zeros`/`np.ones`/`np.arange`/`np.linspace`.
- Index and slice 1-D and 2-D arrays correctly.
- Inspect and convert dtypes; understand why dtype matters.
- Reason about shapes (`(n,)` vs `(n, 1)`).

## 2. Key concepts

- A NumPy **array** is a grid of same-typed numbers with fast, vectorized operations.
- **Vectorization** = operate on whole arrays at once instead of looping.
- **dtype** — every array has one type; mixing types costs memory/speed.
- **Shape** — `(rows, cols)` for 2-D; slicing keeps structure, single indexing removes it.
- Broadcasting (teased here, taught fully in Session 6).
- Pandas and scikit-learn are built on NumPy — learning it pays off everywhere.

## 3. Detailed lecture notes

**Why NumPy?** Show a Python list loop adding 1 to each of a million elements
(`%timeit`) vs. the NumPy one-liner (`arr + 1`). The NumPy version is ~10–100×
faster because operations run on compiled code over contiguous memory — and the
code is shorter. This is *why* the whole data stack is built on it. You don't
replace lists; lists are for small, mixed, flexible data — arrays are for big,
homogeneous, numeric data.

**The array object.** `np.array([1, 2, 3])` from a list. The "nd" in `ndarray`
means n-dimensional: 1-D (vector), 2-D (matrix/table), 3-D (e.g., images). Show
`arr.ndim`, `arr.shape`, `arr.size`, `arr.dtype` — the four facts to know about
any array.

**Creation shortcuts.** Real data is rarely typed by hand; you create arrays from
ranges and patterns: `np.arange(0, 10, 2)`, `np.linspace(0, 1, 5)` (5 evenly
spaced points), `np.zeros((2, 3))`, `np.ones(...)`, `np.full((2,2), 7)`,
`np.eye(3)` (identity). Emphasize `linspace` for plotting axes (Session 13).

**Indexing and slicing.** 1-D: `a[0]`, `a[-1]`, `a[1:4]` (stop excluded), `a[::2]`
(step). 2-D: `a[0, 1]` = row 0, col 1; `a[:, 1]` = whole column; `a[0, :]` =
whole row. Critical subtlety: **slices are views, not copies** — modifying a
slice modifies the original (unlike lists!). Use `.copy()` when you need an
independent array. Also: `a[0, :]` keeps 1-D shape `(cols,)`, while `a[[0], :]`
keeps 2-D — this trips people constantly.

**dtype.** `np.array([1, 2, 3])` → `int64`; add a float → `float64` (upcast).
Explicit: `np.array([1, 2, 3], dtype=np.float32)`. Smaller dtypes save memory on
big datasets. You rarely manage dtype by hand in this course, but you *will* hit
it when reading data with Pandas (Session 8), so know it exists and how to check.

## 4. Important terminology

- **ndarray** — NumPy's n-dimensional array type.
- **Vectorization** — operating on entire arrays at once, avoiding Python loops.
- **dtype** — the element type of an array (`int64`, `float64`, `bool`, …).
- **Shape** — tuple of dimensions, e.g. `(3, 4)` = 3 rows × 4 columns.
- **Axis** — a dimension: axis 0 = rows, axis 1 = columns (for 2-D).
- **Slice** — a view of a portion of an array (`a[1:4]`).
- **View vs copy** — view shares memory with the original; copy doesn't.
- **Upcast** — automatic widening of dtype (int → float) to avoid losing data.

## 5. Python examples

```python
import numpy as np

# Creation
a = np.array([1, 2, 3, 4])
b = np.arange(0, 20, 5)        # [0, 5, 10, 15]
c = np.linspace(0, 1, 5)       # 5 points from 0 to 1
z = np.zeros((2, 3))           # 2x3 matrix of 0.0
m = np.eye(3)                  # identity matrix

print(a.shape, a.dtype, a.ndim)

# Indexing & slicing (1-D)
print(a[0], a[-1])      # 1, 4
print(a[1:3])           # [2 3]
print(a[::2])           # [1 3]

# Indexing & slicing (2-D)
mat = np.array([[1, 2, 3],
                [4, 5, 6]])
print(mat[1, 2])        # 6
print(mat[:, 1])        # column 1 -> [2 5]
print(mat[0, :])        # row 0 -> [1 2 3]

# Views vs copies
view = a[1:3]
view[0] = 99
print(a)                # [1 99 3 4]  <-- original changed!
safe = a[1:3].copy()
safe[0] = 0
print(a)                # unchanged
```

## 6. Beginner example

```python
import numpy as np

scores = np.array([72, 85, 90, 58, 66])
print("Average:", scores.mean())       # 74.2
print("Above 70:", scores[scores > 70])  # boolean mask (preview of S6)
```

Even without knowing NumPy, the code reads like English: "scores greater than 70".

## 7. Practical Data Science example

```python
# A small sensor dataset: temperature readings, one row per day,
# three columns = morning / noon / evening.
temps = np.array([
    [21.0, 24.5, 22.1],   # Monday
    [22.3, 26.0, 23.4],   # Tuesday
    [19.8, 25.1, 21.9],   # Wednesday
    [20.4, 23.9, 22.6],   # Thursday
])

print("Shape:", temps.shape)           # (4, 3) — 4 days, 3 readings
print("Tuesday noon:", temps[1, 1])    # 26.0
print("All noons:", temps[:, 1])       # [24.5 26.0 25.1 23.9]
print("Wednesday:", temps[2, :])       # [19.8 25.1 21.9]
print("Coldest reading:", temps.min())
print("Week's mean:", round(temps.mean(), 2))
```

Mention: when this data arrives as a CSV with headers, Pandas (Sessions 7–8) will
add the column names — NumPy is the engine underneath.

## 8. In-class activity (50 min)

Work in `notebooks/week-03/session-05-numpy-1.ipynb`:

1. **Warm-up (10 min):** create arrays with `arange`, `linspace`, `zeros`, `eye`;
   print `.shape`, `.dtype`, `.ndim` for each.
2. **Slicing drills (20 min):** given a 4×3 matrix, extract (a) the last row,
   (b) the middle column, (c) a 2×2 corner. Predict, then verify.
3. **View/copy experiment (10 min):** modify a slice and show the original changed; fix with `.copy()`.
4. **Speed demo (10 min):** `%timeit` a Python-loop sum of a 1,000,000-element
   array vs. `arr.sum()`. Write one sentence in markdown explaining the difference.

## 9. Lab exercise

Lab 1 (due **Session 6**): `labs/lab-01/` — NumPy arrays: create, inspect,
slice, and summarize arrays, plus checkpoint questions. Starter notebook:
`labs/lab-01/lab-01-starter.ipynb`. **First submission through Git** — commit and
push before the next session.

## 10. Common mistakes

- `np.array([1,2,3], [4,5,6])` — missing brackets; needs `np.array([[1,2,3],[4,5,6]])`.
- Forgetting that slices are views → accidentally mutating source data. Use `.copy()`.
- Confusing rows/cols in 2-D indexing: `a[1, 0]` is row 1, not column 1.
- Using Python lists for numeric work and wondering why it's slow.
- Expecting `a[1:3]` to be a copy like list slicing.
- Ignoring `.shape` errors: "operands could not be broadcast" usually means shapes don't align (fixed in S6).

## 11. Short assessment questions

1. What does `np.arange(2, 10, 3)` produce?
2. `a = np.array([[1,2],[3,4]])` — what is `a[1, 0]`? What is `a[:, 1]`?
3. True/False: modifying a slice of an array also modifies the original array. (True.)
4. Which creation function gives 10 evenly spaced points between 0 and 1?
5. Why is `arr + 1` faster than a Python loop?
6. What is the shape of `np.zeros((2, 3))`?

## 12. CLO mapping

CLO-1: NumPy is the computational foundation for manipulating numeric datasets
— the "Apply Python and standard data science libraries" requirement. Its
concepts (dtype, shape, vectorization) recur in Pandas (Sessions 7–8) and
scikit-learn (Sessions 17–22).

## 13. Suggested homework

- Finish Lab 1 and push it to GitHub (first graded submission).
- Practice: 5 slicing exercises from any NumPy tutorial; verify each with `print`.
- Read: NumPy quickstart (numpy.org/doc/stable/user/quickstart.html) sections 1–4.
- Preview: in a scratch notebook, run `arr = np.random.randint(0, 100, 20)` and
  `arr.mean()`, `arr.std()`, `arr.max()` — Session 6 explains `np.random` fully.