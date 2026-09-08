# Lab 08 — Pandas II: Files, Filtering, Sorting

**Session:** Week 4 · Session 8 · 90 min
**CLO:** CLO-1
**Difficulty:** Beginner

## Learning objectives

By the end of this lab you can:

1. Read and write CSV and JSON files with pandas.
2. Sort with `sort_values` (single and multiple keys, ascending/descending).
3. Chain filtering + sorting into a readable pipeline.
4. Spot and fix a classic "silent dtype" trap when reading files.

## Problem statement

The course's tips dataset must be prepared for a shared team drive: save a
clean CSV, produce a JSON export, and answer three questions about ordering.
A colleague warns you that a previous export "looked fine but the numbers
were strings" — you must verify dtypes after every read.

## Dataset requirements

Seaborn built-in `tips` (244 rows). You will write and re-read your own
`tips-clean.csv` — the file lives in a `datasets/` folder next to your
notebook (create it with `Path("datasets").mkdir(exist_ok=True)`).

## Step-by-step tasks

1. **Load** tips, drop rows with any missing value, and print `shape` and
   dtypes.
2. **Save** `tips.dropna()` to `datasets/tips-clean.csv` with
   `index=False`. Re-read it and confirm the shape is identical — then
   explain why `index=False` matters.
3. **dtype trap:** re-read the CSV and print `df.dtypes`; now read it again
   but check whether `total_bill` is `float64`. If your CSV round-trip
   changed any dtype, note which and why.
4. **Sorting:** show the 5 biggest bills (`sort_values("total_bill",
   ascending=False)`). Then sort by `day` then by `tip` descending
   (two keys).
5. **Filter chain:** `day == "Sun"` with `total_bill > 20`, sorted by tip
   descending — write it as a chained pipeline (one expression).
6. **JSON export:** `df.head(5).to_json("datasets/tips-sample.json",
   orient="records")`, then read it back with `pd.read_json` and confirm
   the shape is `(5, 7)`.
7. **Summary output:** print, from the loaded CSV:
   - the mean tip for `day == "Sat"`,
   - the day with the highest mean bill (`groupby(...).mean()` then
     `idxmax`),
   - the number of rows with `size == 2` and `total_bill > 30`.

## Starter code

```python
import pandas as pd
import seaborn as sns
from pathlib import Path

Path("datasets").mkdir(exist_ok=True)

tips = sns.load_dataset("tips")
clean = tips.dropna()
print("shape after dropna:", clean.shape)

clean.to_csv("datasets/tips-clean.csv", index=False)
back = pd.read_csv("datasets/tips-clean.csv")
print("shape after round-trip:", back.shape)
print(back.dtypes)
# your code here for tasks 4-7
```

## Expected output

- `shape after dropna: (244, 7)`; round-trip also `(244, 7)`.
- dtypes before and after round-trip match (`total_bill`, `tip`: float64;
  `size`: int64; `sex`, `smoker`, `day`, `time`: object).
- 5 biggest bills start at 50.81.
- Filter chain returns 6 rows (Sun, bill > 20), sorted by tip.
- JSON sample re-reads as `(5, 7)`.
- Task 7: Sat mean tip ≈ 2.99; highest mean bill day = Sat; size-2 rows
  with bill > 30: 3 rows.

## Questions

1. What happens without `index=False` when saving a CSV? What appears in the
   file?
2. After a CSV round-trip, which column is most likely to change dtype and
   why?
3. Why does `sort_values` by default put missing values last? How would you
   change that?
4. What does `orient="records"` produce — list of dicts, or dict of lists?
5. Chained pipeline vs. many temporary variables: one advantage of each.

## Challenge task

Rebuild the CSV *without* the `day` column (save `clean.drop(columns=
["day"])`), re-read it, and use `merge` to join the day back from the
original `tips` using the index. Verify the joined frame has 244 rows and a
`day` column. Comment on what the index-based merge assumes.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Load + dropna + shapes | 3 | (244, 7) both times |
| CSV save/read + index=False explained | 3 | explanation correct |
| dtype verification | 3 | comparison before/after |
| Two sort variants | 3 | single key + two keys |
| Chained filter pipeline | 3 | one expression, 6 rows |
| JSON export/import | 2 | (5, 7) |
| Three summary outputs | 3 | values match |
| Answers to questions | 2 | Q1, Q2 correct |
| Challenge: merge back day column | 4 | 244 rows, day present |
| **Total** | **26** | |