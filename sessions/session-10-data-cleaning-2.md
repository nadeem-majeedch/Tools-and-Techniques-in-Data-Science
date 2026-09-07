# Session 10 — Data Cleaning II: Strings, apply, Reshaping

**Week 5 · Session 10 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Clean text columns with the `.str` accessor (`strip`, `lower`, `replace`, `contains`, `split`).
- Apply custom logic to columns/rows with `apply`, `map`, and `transform`.
- Rename columns and values; create derived columns.
- Reshape tables with `melt` and `pivot` / `pivot_table`.
- Recognize "wide vs. long" data and when to convert between them.

## 2. Key concepts

- **Messy text is normal:** whitespace, case, typos, and extra characters corrupt categorical analysis.
- **`.str` accessor** — vectorized string methods; `df["col"].str.strip()` works like `s.strip()` on every element.
- **`apply`/`map`** — run a function per element/row; `map` for simple lookups, `apply` for logic.
- **Derived columns** — `df["new"] = ...` creates analysis-ready features.
- **Wide vs. long** — the two table shapes; `melt` (longer) and `pivot` (wider) convert between them.
- Cleaning is *transformative*: messy → tidy → analysis-ready, each step visible in the notebook.

## 3. Detailed lecture notes

**Why strings?** Real-world columns ("City", "Product", "Email") arrive with
inconsistencies: `"lahore "`, `"Lahore"`, `"LAHORE"` are three values that mean
one thing. `value_counts()` on a dirty text column shows the damage immediately
("Lahore", "lahore", "Lahore ", "LHR"…). The fix pattern: **standardize case →
strip whitespace → replace variants → verify with `value_counts()` again**.

**The `.str` accessor.** `df["name"].str.upper()`, `.str.strip()`,
`.str.replace("Mr.", "")`, `.str.contains("data")` (returns a mask — pairs with
`loc`!), `.str.split(",")` (returns lists — pair with `.str[0]` to take one
piece). Why "accessor"? Because a Series has no `.upper()` method, so `.str`
gives you string methods for the whole column at once. This is vectorization for
text.

**Custom logic with apply/map.** When no built-in method fits: `map` replaces
values via a dict (`{"M": "Male", "F": "Female"}`) — perfect for recoding
categories. `apply` runs a function per element (`df["hours"].apply(np.round)`)
or per row with `axis=1` (function receives each row as a Series — use sparingly;
row-wise apply is slow on big frames, but fine at course scale and infinitely
flexible). Lambda functions keep this concise: `df["score"].apply(lambda x: "pass" if x >= 60 else "fail")`.

**Derived columns.** `df["tip_pct"] = df["tip"] / df["total_bill"] * 100` — new
analysis features are born this way; grouped stats can be attached back with
`transform` (a favorite for "add each row's group mean as a column").

**Reshaping: wide vs. long.** Two layouts for the same data:
- **Wide:** one column per measurement type — easy to read, hard to aggregate (`pivot` output).
- **Long (tidy):** one row per observation — the native shape for `groupby`,
  plotting (Seaborn), and most statistics. The "tidy data" principle: each
  variable is a column, each observation is a row.
`pd.melt(df, id_vars=["day"], value_vars=["mon","tue"], var_name="weekday", value_name="hours")`
turns wide into long; `df.pivot(index=..., columns=..., values=...)` goes the
other way; `pivot_table` = pivot + aggregation (handles duplicate keys). Teach
*melt* first — going long is the more common need.

## 4. Important terminology

- **`.str` accessor** — vectorized string methods on a Series.
- **Whitespace/case normalization** — `.strip()`, `.lower()` on text columns.
- **`apply`** — apply a function to each element (or row/column with `axis`).
- **`map`** — value replacement via a dict.
- **Lambda** — an inline anonymous function: `lambda x: ...`.
- **Derived column** — a new column computed from existing ones.
- **Tidy data** — each variable a column, each observation a row.
- **Wide format** — columns hold distinct measurements; **long format** — rows hold observations.
- **`melt`** — wide → long. **`pivot` / `pivot_table`** — long → wide.
- **`transform`** — broadcast group results back to every row.

## 5. Python examples

```python
import pandas as pd
import seaborn as sns

# --- String cleaning ---
messy = pd.Series(["  Lahore ", "LAHORE", "lahore", " Lhr", "karachi"])
print(messy.str.strip().str.lower().value_counts())

# --- map: recode categories ---
tips = sns.load_dataset("tips")
tips["is_weekend"] = tips["day"].map({"Fri": 0, "Sat": 1, "Sun": 1, "Thur": 0})
print(tips["is_weekend"].value_counts())

# --- apply: custom logic ---
tips["tip_grade"] = tips["tip_pct"].apply(lambda p: "high" if p > 20 else "normal")

# --- derived column ---
tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100

# --- melt: wide -> long ---
wide = pd.DataFrame({"day": ["Mon", "Tue"],
                     "morning": [10, 12],
                     "evening": [15, 18]})
long = pd.melt(wide, id_vars=["day"],
               var_name="shift", value_name="sales")
print(long)

# --- pivot: long -> wide ---
wide_again = long.pivot(index="day", columns="shift", values="sales")
print(wide_again)
```

## 6. Beginner example

```python
import pandas as pd

names = pd.Series(["  AYESHA ", "sara", "USMAN"])
print(names.str.strip().str.title())   # Ayesha Sara Usman
```

Standardizing case and whitespace in one chain — the whole lesson in miniature.

## 7. Practical Data Science example

```python
import pandas as pd

# Messy survey export — the kind of data a colleague would hand you
raw = pd.DataFrame({
    "city":    ["Lahore ", "lahore", "Karachi", "Lahore", " ISB"],
    "hours":   ["3.5", "4", "5.5", "3.5", "4.5"],
    "shift":   ["M", "E", "M", "E", "M"],
})

# 1. Standardize text
raw["city"] = raw["city"].str.strip().str.title().replace({"Isb": "Islamabad"})

# 2. Fix types (values first, then cast)
raw["hours"] = raw["hours"].astype(float)

# 3. Recode with map
raw["shift_full"] = raw["shift"].map({"M": "Morning", "E": "Evening"})

# 4. Derived column
raw["minutes"] = raw["hours"] * 60

# 5. Verify
print(raw)
print(raw["city"].value_counts())
```

## 8. In-class activity (50 min)

In `notebooks/week-05/session-10-cleaning-2.ipynb`:

1. **String cleanup (15 min):** build a messy `city` column (mixed case,
   whitespace, abbreviations); standardize; verify with `value_counts()`.
2. **Recode + derive (15 min):** on `tips`, create `is_weekend` with `map`,
   `tip_pct` as a derived column, and a `tip_grade` with `apply` + lambda.
3. **Reshape lab (20 min):** build a small wide table of your own (e.g., study
   hours by day × shift), `melt` it to long, `pivot` it back; confirm the
   values match. Write a markdown sentence: when is long better than wide?

## 9. Lab exercise

**Lab 2 is due today** (`labs/lab-02/`): Pandas data cleaning. Push before the
deadline. From here on, labs follow the schedule: Lab 3 (Session 12), Lab 4
(Session 14), and so on.

## 10. Common mistakes

- `df["col"].upper()` → AttributeError; you need `.str.upper()`.
- `str.replace` without `str` accessor, or expecting regex-free replacement — `.str.replace` treats patterns as regex by default; use `regex=False` for plain text.
- `apply` on a Series vs DataFrame confusion — Series apply = per element; DataFrame apply with `axis=1` = per row.
- Building one giant lambda that should be a named `def` — readability matters (graders read your code).
- `melt` without `id_vars` → every non-listed column collapses into values.
- Pivoting data with duplicate (index, column) pairs → error; reach for `pivot_table` with an `aggfunc` instead.
- Forgetting to verify after cleaning — run `value_counts()`/`dtypes` again.

## 11. Short assessment questions

1. Why does `df["name"].str.strip()` work while `df["name"].strip()` fails?
2. What does `messy.str.strip().str.lower().value_counts()` accomplish?
3. Write a `map` call converting `{"M": 0, "F": 1}`.
4. What does `df["x"].apply(lambda v: v * 2)` return — a Series or DataFrame? (Series.)
5. `melt` takes data from ___ format to ___ format.
6. When would you use `pivot_table` instead of `pivot`?

## 12. CLO mapping

CLO-1: text cleaning, derived features, and reshaping are core "clean and
manipulate" skills; `melt`/`pivot` are exactly what Assignment 1's reshaping
task exercises. Long-format thinking also underpins Seaborn's plotting API
(Session 14).

## 13. Suggested homework

- Commit the activity notebook.
- Practice: find a messy public CSV (many exist on GitHub "messy data" repos); standardize at least two text columns and reshape the table.
- Read: pandas docs — "Reshaping and pivot tables" (skim the examples).
- Preview: `import requests; r = requests.get("https://jsonplaceholder.typicode.com/todos"); pd.DataFrame(r.json())` — Session 11 explains acquisition from files and APIs.