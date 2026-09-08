# Content for notebook 03: Pandas.
CELLS = [
    ("md", """# 03 — Pandas

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-1 — Apply Python and standard data science libraries to datasets.

Pandas is the workhorse of tabular data in Python. It wraps NumPy arrays with
**labels** — named columns and a row index — so you refer to data by name
(`df["total_bill"]`) instead of by position (`arr[:, 2]`).

---
"""),
    ("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain what a Series and a DataFrame are, and when to use each.
2. Create DataFrames from dicts, lists, and files.
3. Read and write CSV, Excel, and JSON files.
4. Select data with `[]`, `.loc[]`, and `.iloc[]`.
5. Filter rows with conditions and sort results.
6. Inspect data with `info()`, `describe()`, `head()`, `value_counts()`.

---
"""),
    ("code", """# Make sure the datasets/ folder exists next to this notebook.
from pathlib import Path
Path("datasets").mkdir(exist_ok=True)
print("datasets/ ready")
"""),
    ("md", """## Theory: Series vs DataFrame

- A **Series** is a labeled 1-D array: values plus an index (0, 1, 2, ... by
  default). Think of one column of a spreadsheet.
- A **DataFrame** is a labeled 2-D table: each column is a Series, and all
  columns share the same row index. Think of the whole spreadsheet.

Pandas is built on NumPy: every column is an ndarray with a name. Because
each column is its own array, a DataFrame can hold mixed types (numbers,
strings, categories) happily.

---
"""),
    ("code", """import pandas as pd
import numpy as np

# Create a DataFrame from a dict of lists (keys become column names)
students = pd.DataFrame({
    "name":  ["Ali", "Sara", "Usman", "Zara"],
    "score": [82, 91, 68, 95],
    "hours": [3.5, 4.0, 2.0, 5.0],
})
print(students)
print()
print("shape:", students.shape, "| dtypes:")
print(students.dtypes)

# Expected output:
#     name  score  hours
# 0    Ali     82    3.5
# 1   Sara     91    4.0
# 2  Usman     68    2.0
# 3   Zara     95    5.0
#
# shape: (4, 3) | dtypes:
# name     object
# score     int64
# hours   float64
# dtype: object
"""),
    ("md", """## Inspecting data: the first five commands

Before doing anything, *look*. These five commands answer "what is this
table?" and "is it what I expected?":

- `df.head(n)` / `df.tail(n)` — first / last n rows
- `df.info()` — rows, columns, non-null counts, dtypes
- `df.describe()` — summary statistics of numeric columns
- `df["col"].value_counts()` — frequency of each value in a column
- `df.isna().sum()` — missing values per column

---
"""),
    ("code", """import seaborn as sns

tips = sns.load_dataset("tips")     # a real restaurant-tips dataset
print(tips.head(3))
print()
print(tips.info())
print()
print(tips.describe().round(2))
print()
print(tips["day"].value_counts())
"""),
    ("md", """## Selecting data: [], .loc[], .iloc[]

The single most important skill — and the single biggest source of confusion.
The rule of thumb:

- `df["col"]` — a column **by name** (returns a Series).
- `df[["a", "b"]]` — several columns by name (note the double brackets —
  returns a DataFrame).
- `df.loc[label]` or `df.loc[rows, cols]` — selection **by label/index**.
- `df.iloc[pos]` or `df.iloc[rows, cols]` — selection **by integer position**.

Why two systems? Labels survive sorting and filtering (a row named `"Sun"`
stays `"Sun"`), positions do not.

---
"""),
    ("code", """# Column selection
print(tips["tip"].head(3))            # one column -> Series
print()
print(tips[["day", "tip"]].head(2))   # two columns -> DataFrame

# Position-based
print(tips.iloc[0])                   # first row (a Series)
print(tips.iloc[0, 1])                # first row, second column

# Label-based with a condition: the workhorse pattern
big = tips.loc[tips["total_bill"] > 40, ["day", "total_bill", "tip"]]
print(big.head(3))
"""),
    ("md", """## Filtering and sorting

Filtering uses the NumPy boolean-mask idea from notebook 02, applied to named
columns. Sorting orders rows before `head()` when you want "top N".

---
"""),("code", """# Multiple conditions: & (and), | (or) — parentheses required
weekend_big = tips.loc[(tips["day"].isin(["Sat", "Sun"])) & (tips["total_bill"] > 30)]
print("rows:", len(weekend_big))

# Sorting: biggest tips first
top5 = tips.sort_values("tip", ascending=False).head(5)
print(top5[["day", "total_bill", "tip"]])

# Expected output:
#   rows: 78
#        day  total_bill   tip
#   170  Sat       44.30  10.0
#   59   Sat       48.27   9.0
#   175  Sun       32.68   5.0
#   176  Sun       29.80   4.8
#   208  Sat       29.03   4.3
"""),
    ("md", """## Reading and writing files

Real work starts with a file and ends with a file. `read_csv` is the most
common entry point. Two habits from day one:

- Use **relative paths** (relative to the repo root), never absolute machine
  paths — your notebook must run on any machine.
- Pass `index=False` to `to_csv`, or Pandas writes an extra unnamed index
  column you didn't ask for.

---
"""),("code", """# Write the tips data to CSV, then read it back
tips.to_csv("datasets/tips.csv", index=False)
df = pd.read_csv("datasets/tips.csv")
print("read back:", df.shape)

# CSV with a different separator (e.g., semicolon) -> use sep=
df2 = pd.read_csv("datasets/tips.csv", sep=",")
print(df2.shape)

# JSON
tips.head(3).to_json("datasets/tips-sample.json", orient="records")
df3 = pd.read_json("datasets/tips-sample.json")
print(df3.shape)

# Expected output:
#   read back: (244, 7)
#   (244, 7)
#   (3, 7)
"""),
    ("md", """## Beginner example: answers from a DataFrame

Pandas turns questions into one-liners. Ask, then answer — this is the daily
rhythm of data work.

---
"""),("code", """# Questions about the tips dataset, answered in one line each
print("Average bill:", round(tips["total_bill"].mean(), 2))
print("Biggest tip:", tips["tip"].max())
print("Rows where tip > 6:", (tips["tip"] > 6).sum())
print("Most common day:", tips["day"].value_counts().idxmax())
print("Average tip on Sunday:", round(tips.loc[tips["day"] == "Sun", "tip"].mean(), 2))

# Expected output:
#   Average bill: 19.79
#   Biggest tip: 10.0
#   Rows where tip > 6: 3
#   Most common day: Sat
#   Average tip on Sunday: 3.26
"""),
    ("md", """## Intermediate example: the course grading table

A slightly bigger task that uses almost everything above: build a DataFrame,
add a computed column, filter, sort, and save.

---
"""),("code", """import numpy as np

np.random.seed(11)
students = pd.DataFrame({
    "name":   ["Ali", "Sara", "Usman", "Zara", "Bilal", "Hina"],
    "quiz1":  np.random.randint(50, 100, 6),
    "quiz2":  np.random.randint(50, 100, 6),
    "lab":    np.random.randint(40, 100, 6),
})

# Derived column: total out of 300
students["total"] = students["quiz1"] + students["quiz2"] + students["lab"]

# Filter: students who passed (total >= 180), sorted best first
passed = students.loc[students["total"] >= 180].sort_values("total", ascending=False)
print(passed[["name", "total"]])

# Save for later notebooks
students.to_csv("datasets/grades.csv", index=False)
print("saved", students.shape)

# Expected output:
#     name  total
# 2  Usman    273
# 5   Hina    242
# 0    Ali    215
# 1   Sara    215
# 4  Bilal    208
# saved (6, 6)
"""),
    ("md", """## Exercises

---
"""),
    ("md", """### Exercise 1 — Selection

From `tips`, extract (a) the column `"tip"`, (b) rows where `day == "Thur"`,
(c) the `total_bill` and `tip` of rows where `size >= 4`."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
a = tips["tip"]
b = tips[tips["day"] == "Thur"]
c = tips.loc[tips["size"] >= 4, ["total_bill", "tip"]]
print(len(a), len(b), len(c))
# Expected output: 244 62 43
"""),
    ("md", """### Exercise 2 — Info and describe

Run `info()` and `describe()` on `tips`. How many rows? Which columns are
numeric? What is the 75th percentile of `total_bill`? (It is 24.13.)"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
print(tips.describe()["total_bill"]["75%"])
# Expected output: 24.1275
"""),
    ("md", """### Exercise 3 — I/O round trip

Save `tips` to `datasets/tips-out.csv` with `index=False`, read it back, and
confirm the shape is (244, 7)."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
tips.to_csv("datasets/tips-out.csv", index=False)
back = pd.read_csv("datasets/tips-out.csv")
print(back.shape)
# Expected output: (244, 7)
"""),
    ("md", """## Challenge exercise

Using `tips`:

1. Create a new column `"tip_pct"` = `tip / total_bill * 100`, rounded to 1
   decimal.
2. Find the 5 rows with the highest `tip_pct`.
3. Compute the *average* `tip_pct` separately for smokers and non-smokers.
4. Write one markdown sentence explaining what your answer to (3) suggests."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
tips["tip_pct"] = (tips["tip"] / tips["total_bill"] * 100).round(1)

print(tips.nlargest(5, "tip_pct")[["day", "total_bill", "tip", "tip_pct"]])
print()
print(tips.groupby("smoker")["tip_pct"].mean().round(2))
"""),
    ("md", """## Recap

- **DataFrame** = labeled table; **Series** = one labeled column.
- Inspect first: `head`, `info`, `describe`, `value_counts`, `isna`.
- Select by name with `[]` and `.loc[]`; by position with `.iloc[]`.
- Filter with boolean conditions; sort with `sort_values`.
- `read_csv` / `to_csv` are the standard I/O pair — remember `index=False`.
- Derived columns: `df["new"] = ...`.

---
"""),
    ("md", """## Questions

1. What is the difference between `df["score"]` and `df[["score"]]`?
2. When would you use `.iloc` instead of `.loc`?
3. Why pass `index=False` to `to_csv`?
4. What does `df.info()` tell you that `df.head()` does not?
5. What does `df["day"].value_counts()` return — a Series or a DataFrame?
6. Why must conditions in a filter be wrapped in parentheses when using `&`?

---
**Next:** notebook 04 — Data Cleaning: missing values, duplicates, types.
"""),
]