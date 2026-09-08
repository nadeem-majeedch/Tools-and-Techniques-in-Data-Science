# Lab 09 — Data Cleaning I: Missing Values, Duplicates, dtypes

**Session:** Week 5 · Session 9 · 90 min
**CLO:** CLO-1
**Difficulty:** Beginner

## Learning objectives

By the end of this lab you can:

1. Detect missing values with `isna()`/`isnull()` and count them per column.
2. Decide between `dropna` and `fillna` with a stated reason.
3. Find and remove duplicate rows, including near-duplicates on a subset.
4. Convert dtypes deliberately and catch stringy numbers.

## Problem statement

A survey export arrives with classic problems: blank cells, a column that
is secretly text, and duplicated responses (some complete duplicates, some
duplicates on key columns only). You must produce a **cleaning log**: for
every decision, one line saying what you did and **why**.

## Dataset requirements

Build the dirty DataFrame inline (24 rows) — small, reproducible, no files.

## Step-by-step tasks

1. **Build** `raw` from the starter code. Print `raw.info()` and
   `raw.isna().sum()`.
2. **Classify missingness:** which columns have missing values, and how
   many? For `age`, state in your log whether you will drop or fill and
   justify with the mean.
3. **Drop or fill:**
   - Fill `age` with the column mean (rounded to 1 decimal).
   - Drop rows where `city` is missing (only 2 rows — dropping is cheap).
   - Leave `income` missing for now; answer why in your log (see Q2).
4. **Duplicates:** `raw.duplicated().sum()` — drop complete duplicates.
5. **Near-duplicates:** find rows duplicated on `email` only with
   `raw.duplicated(subset=["email"])`, and keep the **first** of each.
   Report how many rows remain.
6. **dtypes:** print dtypes. Convert `age` to `int64` (after filling) and
   explain why that is safe *now* but would have failed before.
7. **Stringy numbers:** `income` contains `"42,500"`-style text. Strip
   commas with `.str.replace(",", "")`, convert to `float`, then state
   whether rows with NaN income should be dropped (drop them — 3 rows).
8. **Final report:** shape of the cleaned frame + the cleaning log as a
   markdown list in a notebook cell.

## Starter code

```python
import pandas as pd
import numpy as np

raw = pd.DataFrame({
    "name":  ["Ali", "Bilal", "Ayesha", "Ali", "Daniyal", "Emaan",
              "Faraz", "Ali", "Hina", "Iqra", "Junaid", "Kiran",
              "Laila", "Mubashir", "Nimra", "Omer", "Ali", "Parveen",
              "Qasim", "Rania", "Sana", "Tariq", "Uzma", "Waqar"],
    "age":   [21, 22, np.nan, 21, 24, 23, np.nan, 21, 22, 25, 21, 24,
              22, np.nan, 23, 26, 21, 24, 22, 23, 21, 25, 22, 24],
    "city":  ["KHI", "LHE", "ISB", "KHI", "KHI", "LHE", "ISB", "KHI",
              "LHE", "KHI", "ISB", np.nan, "KHI", "LHE", "ISB", "KHI",
              "KHI", np.nan, "LHE", "ISB", "KHI", "LHE", "ISB", "KHI"],
    "email": ["a@x.com", "b@x.com", "c@x.com", "a@x.com", "d@x.com", "e@x.com",
              "f@x.com", "a@x.com", "h@x.com", "i@x.com", "j@x.com", "k@x.com",
              "l@x.com", "m@x.com", "n@x.com", "o@x.com", "a@x.com", "p@x.com",
              "q@x.com", "r@x.com", "s@x.com", "t@x.com", "u@x.com", "w@x.com"],
    "income": ["31,000", "45,200", np.nan, "31,000", "52,100", "38,500",
               np.nan, "31,000", "42,800", "60,000", "33,400", "47,900",
               "35,600", "50,000", "41,200", "55,300", "31,000", "48,700",
               "36,900", "43,100", "32,200", "51,600", "34,800", "44,500"],
})

print(raw.info())
print(raw.isna().sum())
# your code here
```

## Expected output

- Missing counts: `age: 3, city: 2, income: 2` (with `name`/`email`: 0).
- After all steps: a cleaned frame of **21 rows** (24 − 1 city-row-drops −
  3 income drops + 0 duplicate drops... compute carefully; the *final*
  shape is deterministic given the steps) with `age` int64 and `income`
  float64, no missing values anywhere (`isna().sum().sum() == 0`).
- A cleaning log with ≥ 6 entries, each "action + reason".

## Questions

1. When is dropping rows with missing values better than filling them?
2. Why leave `income` missing while filling `age`? What principle decides?
3. Why would `astype(int)` fail on a column containing NaN?
4. `duplicated(subset=["email"])` vs `duplicated()` — what's the difference?
5. After `.str.replace(",", "")`, what dtype is the result, and why must
   you convert again?

## Challenge task

Detect **inconsistent city names**: the data also contains `"KHI "` (with
trailing space) and `"Karachi"`. Add three such rows to `raw` yourself,
then normalize `city` with `.str.strip()` plus a `replace` mapping
(`"Karachi" -> "KHI"`), and confirm `value_counts()` shows only 3 distinct
cities. Extend your cleaning log with the normalization step.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Missing-value detection correct | 3 | counts match |
| Drop/fill decisions justified | 4 | log entry per decision |
| Complete + near-duplicate handling | 4 | correct keep-first behavior |
| dtype conversions | 3 | age int64, income float |
| Final shape + zero missing | 3 | (21, 5) or correct variant |
| Cleaning log quality | 4 | ≥6 action+reason entries |
| Answers to questions | 2 | Q3, Q5 correct |
| Challenge: city normalization | 4 | strip + mapping, 3 cities |
| **Total** | **27** | |