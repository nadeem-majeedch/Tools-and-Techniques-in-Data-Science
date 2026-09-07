# Session 8 — Pandas II: I/O, Filtering, groupby

**Week 4 · Session 8 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Read and write CSV, Excel, and JSON files with Pandas (`read_csv`, `to_csv`, etc.).
- Filter rows with multiple conditions and sort results.
- Use `groupby` (split-apply-combine) for grouped summaries.
- Use `value_counts` and `crosstab` for categorical exploration.
- Handle common I/O issues: encodings, missing files, separators.

## 2. Key concepts

- **I/O is one line:** `pd.read_csv("file.csv")` → DataFrame; `df.to_csv(...)` → file.
- **Filtering** = boolean masks on columns (NumPy skill from Session 6, now on named columns).
- **`groupby` = split → apply → combine**: the standard way to summarize by category.
- `value_counts` answers "how many of each category?"; `crosstab` answers "two categories at once".
- **`sort_values`** orders results for readability.
- Real workflow: read → filter/clean → group & summarize → save.

## 3. Detailed lecture notes

**Why I/O first?** Every analysis starts with getting data into a DataFrame.
Pandas reads CSV, Excel, JSON, SQL, Parquet, and more with one function each.
The shape of the lesson: `read_csv` with its most useful arguments, then the
"save your work" counterpart `to_csv`, then the standard workflow verbs.

**Reading files.** `pd.read_csv("path.csv")` — that's it. Useful arguments:
`sep=";"` (European CSVs), `encoding="utf-8"` (fix mojibake), `index_col=0`
(first column as row labels), `parse_dates=["date"]`, `usecols=["a","b"]`.
Trap: relative paths — notebooks should reference files relative to the repo
root, not absolute machine paths (reproducibility!). `pd.read_excel(...)` needs
`openpyxl` (included in `requirements.txt` via pandas extras; install with
`pip install openpyxl` if needed). JSON: `pd.read_json` for arrays of objects;
nested JSON often needs `pd.json_normalize` — mention, don't dwell.

**Writing.** `df.to_csv("out.csv", index=False)` — the `index=False` is the
classic "why are there weird number columns in my file?" fix. Same for Excel.

**Filtering & sorting.** Combine NumPy masks with named columns:
`df.loc[(df["total_bill"] > 30) & (df["day"] == "Sun"), :]`. Remember `&`
needs parentheses around each comparison. `df.sort_values("tip",
ascending=False)` orders results — always sort before `head()` when looking for
"top N".

**groupby — the headline act.** Explain the name: **split** the table by unique
values of a column (e.g., `day`), **apply** a function to each group
(`tip.mean()`), **combine** into a new table indexed by group. Show the mental
picture: 244 rows → 4 groups → one row per day. Then extend: group by two
columns `df.groupby(["day", "sex"])` → one row per (day, sex) pair. Common
pitfall: `df.groupby("day")` alone does nothing visible until you aggregate.
`agg` with a list of functions (`["mean", "count"]`) is a power move —
introduce lightly.

**Categorical exploration.** `df["day"].value_counts()` — how many bills per
day, sorted descending. `pd.crosstab(df["day"], df["sex"])` — a two-way count
table. Both feed directly into plotting in Sessions 13–14.

## 4. Important terminology

- **CSV / TSV** — comma/tab-separated values, the universal data exchange format.
- **`read_csv` / `to_csv`** — Pandas I/O entry/exit points.
- **`index=False`** — omit the row-index column when saving.
- **Split-apply-combine** — the `groupby` pattern.
- **`value_counts`** — frequency table for one categorical column.
- **`crosstab`** — frequency table for two categorical columns.
- **`sort_values`** — order rows by one or more columns.
- **Encoding** — how text is stored as bytes; `utf-8` is the modern default.
- **`parse_dates`** — tell Pandas a column contains dates (so it becomes `datetime64`).

## 5. Python examples

```python
import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")          # stand-in for a CSV you'd read

# --- I/O ---
tips.to_csv("datasets/tips.csv", index=False)          # write
df = pd.read_csv("datasets/tips.csv")                  # read back
print(df.shape)

# --- Filtering with multiple conditions ---
sun_big = tips.loc[(tips["day"] == "Sun") & (tips["total_bill"] > 25)]
print(sun_big.head())

# --- Sorting ---
top5 = tips.sort_values("tip", ascending=False).head(5)
print(top5[["day", "total_bill", "tip"]])

# --- groupby: split-apply-combine ---
by_day = tips.groupby("day")["tip"].mean()
print(by_day)

# Two columns at once
two = tips.groupby(["day", "sex"])["tip"].mean().round(2)
print(two)

# --- Categorical summaries ---
print(tips["day"].value_counts())
print(pd.crosstab(tips["day"], tips["sex"]))
```

## 6. Beginner example

```python
import pandas as pd

prices = pd.DataFrame({"fruit": ["apple", "banana", "apple"],
                       "price": [80, 30, 90]})
print(prices.groupby("fruit")["price"].mean())
```

Split by `fruit`, average each group, combine — the entire `groupby` idea in one
line, readable as a sentence.

## 7. Practical Data Science example

```python
import pandas as pd
import seaborn as sns

# Realistic: "Which day and party size generate the biggest tips?"
tips = sns.load_dataset("tips")

# Step 1: clean-ish preview
print(tips.info())

# Step 2: explore categories
print(tips["day"].value_counts())
print(pd.crosstab(tips["day"], tips["smoker"]))

# Step 3: grouped summary with multiple stats
summary = tips.groupby("day")["tip"].agg(["mean", "median", "count"]).round(2)
print(summary.sort_values("mean", ascending=False))

# Step 4: filtered deep-dive
big_parties = tips[tips["size"] >= 4]
print(big_parties.groupby("day")["total_bill"].mean().round(2))

# Step 5: save the summary for the report
summary.to_csv("datasets/tip-summary-by-day.csv")
```

## 8. In-class activity (50 min)

In `notebooks/week-04/session-08-pandas-2.ipynb`:

1. **I/O round-trip (10 min):** save `tips` to `datasets/tips.csv` (with
   `index=False`), read it back, confirm `shape` matches, then read the raw file
   in a text editor to see what `index=False` changed.
2. **Filter + sort (15 min):** answer: (a) the 5 largest bills on Friday;
   (b) average tip of non-smoker parties of 2; (c) count of bills over $40 by day.
3. **groupby practice (15 min):** mean tip by day and by `sex`; then
   `groupby(["sex", "smoker"])["tip"].mean()` — write the story in markdown.
4. **crosstab (10 min):** `pd.crosstab(tips["day"], tips["size"])` — which day
   has the most 4-person parties?

## 9. Lab exercise

No lab due today — but from **Session 10 on**, labs are due per the schedule.
Next graded lab: **Lab 2** (data cleaning, due Session 10). Today's activity
notebook is the practice ground; commit it before you leave.

## 10. Common mistakes

- `df.to_csv("x.csv")` without `index=False` → mysterious unnamed column on reload.
- Reading a file with a different separator → one column with everything; check `sep`.
- Grouping and forgetting to aggregate: `tips.groupby("day")` → prints nothing useful.
- `df.groupby("day")["tip"]` returns a GroupBy object — you need `.mean()`/`.sum()` etc.
- Filtering with `and` instead of `&`, or missing parentheses around conditions.
- Sorting descending with `ascending=True` accidentally and blaming the data.
- Not setting `parse_dates=True`/`parse_dates=["col"]` and later doing string math on dates.

## 11. Short assessment questions

1. Why do we pass `index=False` to `to_csv`?
2. Write the expression: rows where `day == "Sun"` AND `total_bill > 20`, only columns `day` and `tip`.
3. What three steps does `groupby` perform (in order)?
4. What does `tips.groupby("day")["tip"].mean()` return — a Series or DataFrame? (Series, indexed by day.)
5. What does `df["day"].value_counts()` tell you?
6. Your CSV loads with one giant column — what is likely wrong, and what argument fixes it?

## 12. CLO mapping

CLO-1: file I/O, filtering, and grouped aggregation are the bread-and-butter of
"acquire, manipulate, and explore datasets". These exact verbs power Assignment 1
(cleaning + manipulation, due Session 15) and the EDA case study (Session 15).

## 13. Suggested homework

- Commit the activity notebook.
- Practice: download any small public CSV (e.g., a sports or weather dataset) and run `read_csv` → `groupby` → `to_csv` on it.
- Read: pandas docs — "Group by: split-apply-combine" (10 minutes).
- Preview: `print(tips.isna().sum())` and `print(tips.duplicated().sum())` — Session 9 explains what you're looking at: missing values and duplicates.