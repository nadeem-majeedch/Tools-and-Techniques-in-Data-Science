# Content for notebook 04: Data Cleaning.
CELLS = [
    ("md", """# 04 — Data Cleaning

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-1 — Apply Python and standard data science libraries to datasets.

In industry, cleaning routinely takes 60–80% of a project's time. Every
downstream step — EDA, models, AI assistants — silently assumes clean input.
This notebook teaches the cleaning loop: **look → decide → apply → verify**.

---
"""),
    ("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Detect missing values with `isna()` / `notna()`.
2. Choose between `dropna()` and `fillna()` with justification.
3. Find and remove duplicate rows with `duplicated()` / `drop_duplicates()`.
4. Diagnose and fix wrong dtypes with `astype` and `pd.to_datetime`.
5. Clean text columns with the `.str` accessor.
6. Apply custom logic with `apply` and `map`, and reshape with `melt`/`pivot`.

---
"""),
    ("md", """## Theory: garbage in, garbage out

A model trained on data with 30% missing values in one column isn't "wrong" —
it is silently learning a distorted pattern. Cleaning is where you earn trust
in your numbers. The key mindset: **before deciding what to do with missing
values, ask WHY they are missing**:

- *Missing completely at random* (a sensor dropped a reading) → safe to drop
  or fill with the mean.
- *Missing systematically* (e.g., salary blank for the highest earners) →
  dropping would bias your analysis. The missingness itself is information.

Rule of thumb: never `dropna()` everything by default; drop on the columns
that matter, and justify every choice in a comment.

---
"""),("code", """import pandas as pd
import numpy as np

# A deliberately messy dataset - the kind a colleague hands you
df = pd.DataFrame({
    "name":  ["Ali", "Sara", "Usman", "Ali", None],
    "score": [82, None, 68, 82, 91],
    "date":  ["2024-01-05", "2024-01-06", "2024-01-07", "2024-01-05", "2024-01-08"],
    "grade": ["B", "A", "C", "B", "A"],
})
print(df)
print()
print(df.isna().sum())           # missing per column
print("duplicate rows:", df.duplicated().sum())
"""),
    ("md", """## Missing values: detect, decide, apply

---
"""),("code", """# LOOK
print(df.isna().sum())

# DECIDE
#   - "score" is missing once: drop only rows missing the KEY column.
#   - Duplicates defined by ALL columns: drop them.
#   - The missing name: fill with "unknown" (explicit, honest).
#   - "grade" can be derived from score later - keep as is for now.

# APPLY
df_clean = df.dropna(subset=["score"])       # rows where score is present
df_clean = df_clean.drop_duplicates()
df_clean["name"] = df_clean["name"].fillna("unknown")

# VERIFY
print(df_clean.isna().sum())
print(df_clean)

# Expected output:
#   name     1
#   score    1
#   date     0
#   grade    0
#   dtype: int64
#   name     0
#   score    0
#   date     0
#   grade    0
#   dtype: int64
#       name  score        date grade
#   0     Ali     82  2024-01-05     B
#   1    Sara     91  2024-01-06     A
#   2   Usman     68  2024-01-07     C
"""),
    ("md", """## Fixing types: values first, then cast

A column of numbers stored as text blocks all math (`describe()` gives
nothing). A column of dates stored as text blocks time analysis. The rule:
**clean the values first, then cast the type** — casting before cleaning
produces confusing errors.

---
"""),("code", """# Bad types: numbers as text, dates as text
messy = pd.DataFrame({
    "price": ["12.50", "9.99", "N/A", "15.00"],
    "when":  ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
})
print(messy.dtypes)
print(messy["price"].astype(float, errors="ignore").describe())

# 1. Clean values: replace the "N/A" text with a real missing value
messy["price"] = pd.to_numeric(messy["price"], errors="coerce")

# 2. Fix types
messy["price"] = messy["price"].astype(float)
messy["when"] = pd.to_datetime(messy["when"])

print()
print(messy.dtypes)
print(messy["price"].mean())
"""),
    ("md", """## Text cleaning with the .str accessor

Real text columns arrive inconsistent: `"Lahore "`, `"LAHORE"`, `"Lahore"`
mean one thing but count as three. The fix pattern: **standardize case →
strip whitespace → replace variants → verify with `value_counts()`**.

---
"""),("code", """cities = pd.Series(["  Lahore ", "LAHORE", "lahore", " Lhr", "karachi", "ISB"])

cleaned = cities.str.strip()          # remove surrounding spaces
cleaned = cleaned.str.title()         # "Lahore" style
cleaned = cleaned.replace({"Lhr": "Lahore", "Isb": "Islamabad"})

print(cleaned)
print()
print(cleaned.value_counts())

# Expected output:
#   0        Lahore
#   1        Lahore
#   2        Lahore
#   3        Lahore
#   4       Karachi
#   5    Islamabad
#   dtype: object
#
#   Lahore       4
#   Karachi      1
#   Islamabad    1
#   Name: count, dtype: int64
"""),
    ("md", """## apply and map: custom logic

When no built-in method fits, run your own logic per element:

- `map(dict)` — replace values via a lookup table (recoding categories).
- `apply(func)` — run a function on every element (or row, with `axis=1`).
- Lambda functions (`lambda x: ...`) keep this concise.

---
"""),("code", """import seaborn as sns

tips = sns.load_dataset("tips")

# map: recode categories
tips["is_weekend"] = tips["day"].map({"Fri": 0, "Sat": 1, "Sun": 1, "Thur": 0})
print(tips["is_weekend"].value_counts().sort_index())

# apply: custom logic per element
tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100
tips["tip_level"] = tips["tip_pct"].apply(lambda p: "high" if p > 20 else "normal")
print(tips["tip_level"].value_counts())

# Expected output:
#   0    128
#   1    116
#   Name: count, dtype: int64
#   normal    202
#   high       42
#   Name: count, dtype: int64
"""),
    ("md", """## Reshaping: wide vs long (melt and pivot)

The same data can live in two layouts:

- **Wide:** one column per measurement (easy to read, hard to aggregate).
- **Long (tidy):** one row per observation — the native shape for `groupby`
  and for Seaborn plotting.

`melt` goes wide → long; `pivot` goes long → wide. Going long (`melt`) is the
more common need.

---
"""),("code", """# Wide: sales by shift in separate columns
wide = pd.DataFrame({
    "day":     ["Mon", "Tue", "Wed"],
    "morning": [10, 12, 9],
    "evening": [15, 18, 14],
})
print("WIDE:")
print(wide)

# melt -> long (tidy)
long = pd.melt(wide, id_vars=["day"],
               var_name="shift", value_name="sales")
print("\\nLONG (after melt):")
print(long)

# pivot -> back to wide
wide_again = long.pivot(index="day", columns="shift", values="sales")
print("\\nWIDE (after pivot):")
print(wide_again)
"""),
    ("md", """## Beginner example: the full cleaning loop on real data

The penguins dataset has documented missing values — a perfect practice
target. Run the loop: look → decide → apply → verify.

---
"""),("code", """import seaborn as sns

df = sns.load_dataset("penguins")
print("BEFORE:")
print(df.isna().sum())

# DECIDE:
#   - Bill measurements missing: drop rows missing the KEY columns.
#   - sex missing: "could not determine" - fill with mode.
df_clean = df.dropna(subset=["species", "bill_length_mm", "bill_depth_mm"])
df_clean["sex"] = df_clean["sex"].fillna(df_clean["sex"].mode()[0])

print("\\nAFTER:")
print(df_clean.isna().sum())
print("rows kept:", len(df_clean), "of", len(df))

# Expected output:
#   BEFORE:
#   species              0
#   island               0
#   bill_length_mm       2
#   bill_depth_mm        2
#   flipper_length_mm    2
#   body_mass_g          2
#   sex                 11
#   dtype: int64
#
#   AFTER:
#   species              0
#   island               0
#   bill_length_mm       0
#   bill_depth_mm        0
#   flipper_length_mm    2
#   body_mass_g          2
#   sex                  0
#   dtype: int64
#   rows kept: 342 of 344
"""),
    ("md", """## Intermediate example: cleaning a messy export

A realistic "survey export" with every problem type in one table.

---
"""),("code", """raw = pd.DataFrame({
    "city":  ["Lahore ", "lahore", "Karachi", "Lahore", " ISB"],
    "hours": ["3.5", "4", "5.5", "3.5", "4.5"],
    "shift": ["M", "E", "M", "E", "M"],
})

# 1. Standardize text (case + whitespace + variants)
raw["city"] = raw["city"].str.strip().str.title().replace({"Isb": "Islamabad"})

# 2. Fix types - clean values first, then cast
raw["hours"] = pd.to_numeric(raw["hours"], errors="coerce")

# 3. Recode with map
raw["shift_full"] = raw["shift"].map({"M": "Morning", "E": "Evening"})

# 4. Derived column
raw["minutes"] = raw["hours"] * 60

# 5. Verify
print(raw)
print(raw["city"].value_counts())

# Expected output:
#         city  hours  shift shift_full  minutes
# 0     Lahore    3.5      M    Morning    210.0
# 1     Lahore    4.0      E    Evening    240.0
# 2    Karachi    5.5      M    Morning    330.0
# 3     Lahore    3.5      E    Evening    210.0
# 4  Islamabad    4.5      M    Morning    270.0
# Lahore       3
# Karachi      1
# Islamabad    1
# Name: count, dtype: int64
"""),
    ("md", """## Exercises

---
"""),
    ("md", """### Exercise 1 — Missing values

For the `penguins` dataset: how many rows have at least one missing value?
(*Hint:* `df.isna().any(axis=1).sum()`). Then drop rows missing `sex` only."""),
    ("code", """import seaborn as sns
df = sns.load_dataset("penguins")

# your code here
"""),
    ("code", """# Solution
print("rows with any missing:", df.isna().any(axis=1).sum())
no_sex = df.dropna(subset=["sex"])
print("rows after dropping missing sex:", len(no_sex))
# Expected output:
#   rows with any missing: 11
#   rows after dropping missing sex: 333
"""),
    ("md", """### Exercise 2 — Duplicates

Create a DataFrame with a row repeated twice; remove duplicates and confirm
the count."""),
    ("code", """import pandas as pd

df = pd.DataFrame({"a": [1, 2, 2, 3, 3, 3], "b": ["x", "y", "y", "z", "z", "z"]})

# your code here
"""),
    ("code", """# Solution
print("before:", len(df))
df = df.drop_duplicates()
print("after:", len(df))
# Expected output:
#   before: 6
#   after: 3
"""),
    ("md", """### Exercise 3 — Text cleaning

From `messy = pd.Series(["  python ", "PYTHON", "pandas", " numpy"])`,
produce the counts `python 2, pandas 1, numpy 1`."""),
    ("code", """import pandas as pd
messy = pd.Series(["  python ", "PYTHON", "pandas", " numpy"])

# your code here
"""),
    ("code", """# Solution
clean = messy.str.strip().str.lower()
print(clean.value_counts())
# Expected output:
#   python    2
#   numpy     1
#   pandas    1
#   Name: count, dtype: int64
"""),
    ("md", """## Challenge exercise

The `titanic` dataset (`sns.load_dataset("titanic")`) needs cleaning before
any modeling:

1. Report missing values per column.
2. Fill missing `age` with the **median age** (justify: age is roughly
   symmetric, median is robust).
3. Drop rows missing `embark_town` (only a couple — the key column).
4. Convert `who` (man/woman/child) to a numeric code 0/1/2 with `map`.
5. Verify: no missing values remain in `age` and `embark_town`.

Use the cleaning loop (look → decide → apply → verify) and comment every
decision."""),
    ("code", """import seaborn as sns
titanic = sns.load_dataset("titanic")

# your code here
"""),
    ("code", """# Solution
print("BEFORE:")
print(titanic.isna().sum())

t = titanic.copy()
t["age"] = t["age"].fillna(t["age"].median())            # 2
t = t.dropna(subset=["embark_town"])                     # 3
t["who_code"] = t["who"].map({"man": 0, "woman": 1, "child": 2})  # 4

print("\\nAFTER (key columns):")
print(t[["age", "embark_town", "who_code"]].isna().sum())  # 5

# Expected output:
#   BEFORE:
#   survived         0
#   pclass           0
#   sex              0
#   age            177
#   sibsp            0
#   parch            0
#   fare             0
#   embarked         2
#   class            0
#   who              0
#   adult_male       0
#   deck           688
#   embark_town      2
#   alive            0
#   alone            0
#   dtype: int64
#
#   AFTER (key columns):
#   age            0
#   embark_town    0
#   who_code       0
#   dtype: int64
"""),
    ("md", """## Recap

- Cleaning loop: **look → decide → apply → verify** — every step documented.
- Missing values: ask *why* before choosing `dropna` vs `fillna`.
- Duplicates: decide which columns define a unique record (`subset=`).
- Types: clean values first, then `astype` / `pd.to_datetime`.
- Text: `.str.strip().str.lower()` + `replace` for variants.
- Custom logic: `map` for recoding, `apply` for functions.
- Reshape: `melt` (wide → long), `pivot` (long → wide).

---
"""),
    ("md", """## Questions

1. Why is `dropna()` without thought dangerous on wide tables?
2. When is filling missing values with the mean wrong?
3. What does `df.drop_duplicates(subset=["id"])` do differently from `drop_duplicates()`?
4. Why does `astype(int)` crash on a column containing "N/A"?
5. What is the difference between `map` and `apply`?
6. When would you use `pivot_table` instead of `pivot`?

---
**Next:** notebook 05 — Data Aggregation: groupby, merge, concat.
"""),
]