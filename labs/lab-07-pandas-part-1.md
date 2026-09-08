# Lab 07 — Pandas I: Series, DataFrame, Selection

**Session:** Week 4 · Session 7 · 90 min
**CLO:** CLO-1
**Difficulty:** Beginner

## Learning objectives

By the end of this lab you can:

1. Build Series and DataFrames from dicts and lists.
2. Use `.loc[]` (labels) and `.iloc[]` (positions) correctly.
3. Filter rows with boolean conditions and `isin`.
4. Use `info()`, `describe()`, `value_counts()`, `nunique()` for a first look.

## Problem statement

Your team tracks course enrollments across four programs in a small
DataFrame. Before any modeling, you must demonstrate mastery of labeled
selection: answer five questions about the data using `.loc`/`.iloc` and
boolean masks — no guessing from raw printing.

## Dataset requirements

Build the DataFrame inline from the dict below (24 rows, hand-made but
realistic). No files.

## Step-by-step tasks

1. **Build** `df` from the dict below. Print `info()` and `describe()`.
2. **Label selection:** use `.loc` to show rows where `program == "DS"`.
3. **Position selection:** use `.iloc` to show the last 3 rows, and the
   single value at row 5, column `"enrolled"` — look up how `.iloc` handles
   columns by position.
4. **Filtering:** show rows with `enrolled > 80`, then rows with
   `enrolled > 80` **and** `year >= 2022` (remember the `&` and
   parentheses).
5. **Categorical filter:** show rows where `semester` is in
   `["Fall", "Spring"]` using `.isin`.
6. **First look:** print `value_counts()` for `program` and `nunique()` for
   `semester`.
7. **Add a column:** `df["fill_rate"] = df["enrolled"] / df["capacity"]`,
   rounded to 2 decimals, and show the 3 highest fill rates with
   `nlargest`.

## Starter code

```python
import pandas as pd

df = pd.DataFrame({
    "program": ["DS", "DS", "DS", "DS", "DS", "DS", "DS", "DS",
                "AI", "AI", "AI", "AI", "AI", "AI", "AI", "AI",
                "CS", "CS", "CS", "CS", "CS", "CS", "CS", "CS"],
    "year":    [2021, 2021, 2022, 2022, 2023, 2023, 2024, 2024] * 3,
    "semester": ["Fall", "Spring"] * 12,
    "enrolled": [55, 48, 62, 58, 70, 66, 85, 79,
                 40, 35, 45, 42, 52, 49, 60, 55,
                 90, 85, 95, 88, 100, 92, 110, 102],
    "capacity": [80, 80, 80, 80, 80, 80, 100, 100] * 3,
})

print(df.info())
print(df.describe())
# your code here for tasks 2-7
```

## Expected output

- `info()`: 24 rows, 5 columns, no nulls, dtypes `object/int64`.
- Task 2: 8 rows, all `program == "DS"`.
- Task 3: 3 rows; the value at row 5 / col `"enrolled"` is a single int
  (58 with this data).
- Task 4: rows with enrolled > 80 → 4 rows; with year ≥ 2022 → 4 rows.
- Task 5: 16 rows (Fall + Spring = all of them).
- Task 6: `DS 8, AI 8, CS 8` and `nunique() == 2`.
- Task 7: fill rates; the top-3 rows come from CS, with the 2024 Fall CS
  row at or near the top.

## Questions

1. What is the difference between `.loc[5]` and `.iloc[5]` on this df?
2. Why must conditions be wrapped in parentheses when combined with `&`?
3. When is `.isin()` clearer than multiple `==` conditions?
4. Why does `df["enrolled"] > 80` produce a Series of booleans? What does
   pandas do with it in `df[condition]`?
5. `df["fill_rate"]` — why is bracket access enough for a single column?

## Challenge task

Without loops, compute the **average fill rate per program** (group by
`program`, mean of `fill_rate`, rounded to 3) and print it sorted descending.
Then find the program–semester combination with the single highest fill
rate using `idxmax` on `fill_rate`. Comment on what `idxmax` returns (an
index label, not a value).

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| DataFrame built + info/describe | 3 | 24×5, correct dtypes |
| `.loc` program filter | 2 | 8 rows |
| `.iloc` last rows + single value | 3 | value 58 |
| Boolean filters (single + `&`) | 3 | 4 rows + 4 rows |
| `.isin` filter | 2 | 16 rows |
| value_counts/nunique | 2 | correct counts |
| fill_rate column + nlargest | 3 | top-3 correct |
| Answers to questions | 2 | Q1, Q2 correct |
| Challenge: groupby mean + idxmax | 4 | descending order + index label |
| **Total** | **24** | |