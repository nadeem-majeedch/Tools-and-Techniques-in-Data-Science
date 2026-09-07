# Session 7 — Pandas I: Series & DataFrame

**Week 4 · Session 7 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Explain what a DataFrame is and why it is the central object of data science.
- Create Series and DataFrames from dicts, lists, and NumPy arrays.
- Read key attributes: `shape`, `columns`, `index`, `dtypes`, `head`, `tail`.
- Select data with `[]`, `.loc[]`, and `.iloc[]`, and explain when each applies.
- Compare Series/DataFrame with NumPy arrays and Python lists.

## 2. Key concepts

- A **DataFrame** = labeled table: named columns, labeled rows (index).
- A **Series** = one labeled column; the DataFrame is a collection of Series.
- **`[]` by column name** → `df["col"]`; **`loc`** → labels; **`iloc`** → positions.
- **`df.groupby(...)`** — split-apply-combine: the core aggregation tool (previewed, formalized in Session 8).
- Pandas wraps NumPy — every column is an ndarray with a name.
- Mixed types live happily in a DataFrame because columns are separate arrays.

## 3. Detailed lecture notes

**Why Pandas?** NumPy arrays are fast but anonymous: column 2, row 5 — no names.
Real datasets come with headers, dates, categories, missing values, and 100,000
rows. Pandas adds **labels** on top of NumPy: `df["total_bill"]` instead of
`arr[:, 2]`. That single idea — referring to data by name — is why Pandas is the
industry standard for tabular data.

**Series vs DataFrame.** A Series is a labeled 1-D array: values plus an index
(0, 1, 2… by default). A DataFrame is a labeled 2-D table: each column is a
Series; columns share the same index. Build one from a dict of lists
(keys = column names) or a list of dicts (each dict = a row). DataFrame ≈
spreadsheet with superpowers; Series ≈ one column of that spreadsheet.

**Three ways to select.** This is the #1 skill and #1 confusion:
- `df["col"]` — column by name; `df[["a", "b"]]` — several columns (note double brackets → DataFrame).
- `df.loc["label"]` or `df.loc[["r1","r2"], "col"]` — selection by **label** (row names).
- `df.iloc[0]` or `df.iloc[0:3, 1]` — selection by **integer position**.
Rule of thumb: you know the column name → `[]` or `loc`; you know the position or
want the first N rows → `iloc`. Mixed `df.loc[:, "col"]` means "all rows, this column".

**Why both?** Real data has meaningful labels (dates, IDs); positions change when
you sort or filter. Label-based selection survives reordering; positional doesn't.
Show a filtering example: `df.loc[df["tip"] > 5, ["day", "tip"]]` — rows where a
condition holds, restricted columns. This one expression contains most of
Pandas' power: condition + selection.

**Attributes to know.** `df.shape` (rows, cols), `df.columns`, `df.index`,
`df.dtypes` (per-column dtype), `df.head(n)`/`df.tail(n)`, `df.info()` (summary:
rows, columns, non-null counts, dtypes — essential for cleaning in Session 9).

**dtypes recap from NumPy.** Each column has its own dtype. A column of strings
is `object`; mixing numbers and text in one column makes the whole column
`object` — a classic cleaning issue (Session 9).

## 4. Important terminology

- **DataFrame** — labeled 2-D table (rows = observations, columns = features).
- **Series** — labeled 1-D array; a single column.
- **Index** — the row labels (default 0,1,2…; can be dates, names, etc.).
- **`.loc[]`** — label-based selection (rows and/or columns).
- **`.iloc[]`** — position-based selection.
- **Column dtype** — per-column type: `int64`, `float64`, `bool`, `object`, `datetime64`.
- **`groupby`** — split data by a column's values, apply a function to each group, combine results.
- **`head`/`tail`** — first/last N rows (default 5).
- **NaN** — "Not a Number", Pandas' marker for missing values (Session 9).

## 5. Python examples

```python
import pandas as pd
import numpy as np

# --- Build a DataFrame ---
students = pd.DataFrame({
    "name": ["Ali", "Sara", "Usman", "Zara"],
    "score": [82, 91, 68, 95],
    "hours": [3.5, 4.0, 2.0, 5.0],
})
print(students)
print(students.shape)        # (4, 3)
print(students.dtypes)

# --- Selection ---
print(students["score"])                 # Series
print(students[["name", "score"]])       # DataFrame
print(students.loc[1])                   # row labeled 1
print(students.iloc[0, 1])               # first row, second column -> 82
print(students.loc[students["score"] > 80, ["name", "score"]])  # condition + columns

# --- Series from NumPy ---
s = pd.Series(np.array([1, 2, 3]), name="values")
print(s.mean(), s.max())
```

## 6. Beginner example

```python
import pandas as pd

# Dict of lists: keys become columns
tips = pd.DataFrame({
    "day":   ["Fri", "Sat", "Sun", "Sun"],
    "total": [16.99, 44.30, 20.65, 35.76],
    "tip":   [1.01,  3.50,  3.50,  5.65],
})
print(tips["tip"].mean())          # 3.415
print(tips[tips["total"] > 20])    # rows where the bill was large
```

Two verbs — mean of a column, filter rows — and you've started doing real work.

## 7. Practical Data Science example

```python
import seaborn as sns
import pandas as pd

tips = sns.load_dataset("tips")
print(tips.info())
print(tips.head(3))

# Typical first exploration questions
print("Average bill:", round(tips["total_bill"].mean(), 2))
print("Max tip:", tips["tip"].max())

# Split-apply-combine preview: mean tip by day (formalized next session)
print(tips.groupby("day")["tip"].mean())

# Condition + column selection: big weekend bills
big = tips.loc[tips["total_bill"] > 40, ["day", "total_bill", "tip"]]
print(big.head())
```

## 8. In-class activity (50 min)

In `notebooks/week-04/session-07-pandas-1.ipynb`:

1. **Build (10 min):** create a DataFrame of 5 of your classmates: `name`,
   `program`, `gpa`, `credits`. Print `.shape`, `.dtypes`, `.head()`.
2. **Selection drills (20 min):** using `tips`: (a) select only `tip`; (b) first
   3 rows with `iloc`; (c) row where `tip` is max using `loc` with a condition;
   (d) the `day` and `tip` of bills over $30. Predict each result before running.
3. **groupby taste (10 min):** `tips.groupby("sex")["tip"].mean()` — write a
   markdown sentence about what it shows.
4. **Checkpoint (10 min):** answer two short-answer questions in markdown:
   "When would you use `loc` instead of `iloc`?" and "What does `df["col"]`
   return vs `df[["col"]]`?"

## 9. Lab exercise

No lab due this session (Lab 2 comes after cleaning, Session 10). **Quiz 1 today**
(covers Python + NumPy, Sessions 1–6) — see `../quizzes/quiz-01`.

## 10. Common mistakes

- `df["col", "col2"]` → error; need double brackets `df[["col", "col2"]]`.
- Using `df.iloc["name"]` with a label — `iloc` takes positions only.
- Chained indexing `df[df.x > 5]["y"]` — works but can silently warn/break; prefer `.loc[condition, "y"]`.
- Forgetting `.head()` and printing 1,000-row frames in class demos.
- Modifying a copy: `sub = df[df.x > 5]; sub["new"] = ...` warns "SettingWithCopy" — operate on the filtered frame directly or `.copy()`.
- Confusing Series `.mean()` (column mean) with DataFrame `.mean()` (column means) — DataFrame returns a Series of means.

## 11. Short assessment questions

1. What is the difference between `df["score"]` and `df[["score"]]`?
2. `df.iloc[2, 1]` — position or label based?
3. What does `df.shape` return for a DataFrame with 10 rows and 4 columns?
4. Write one line that returns the rows where `score > 80`, keeping only `name` and `score`.
5. What does `.loc[2]` return — a Series or a DataFrame? (Series — one row.)
6. Why might a column intended to hold numbers have dtype `object`? (It contains some non-numeric values.)

## 12. CLO mapping

CLO-1: DataFrame selection and manipulation are the core "manipulate datasets"
skill. This session is the pivot from generic Python/NumPy to the Pandas
workflow that the rest of Module A (and Assignment 1) is built on.

## 13. Suggested homework

- Finish the activity notebook; commit to your repo.
- Practice: using `tips`, answer 5 of your own questions with one `loc`-style expression each.
- Read: pandas "10 minutes to pandas" (pandas.pydata.org) — the *Getting data in/out* and *Selection* sections.
- Preview: `pd.read_csv("datasets/...")` if you have a CSV, or read on in the docs — Session 8 covers file I/O and `groupby` fully.