# Session 9 — Data Cleaning I: Missing Values, Duplicates, Types

**Week 5 · Session 9 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Explain why cleaning is the largest share of real data work.
- Detect missing values with `isna`/`isnull` and summarize with `.sum()`.
- Choose and apply `dropna` vs. `fillna` appropriately.
- Find and remove duplicate rows with `duplicated`/`drop_duplicates`.
- Diagnose and fix wrong dtypes with `astype` and `to_datetime`.
- Reason about *why* data is missing before deciding what to do.

## 2. Key concepts

- **Garbage in, garbage out:** models and charts inherit data problems — cleaning is not optional.
- **Missing values** come in kinds: missing at random vs. systematically missing (e.g., "left blank if no answer"). The kind drives the fix.
- **Drop vs. fill** is a trade-off: dropping loses information; filling invents information.
- **Duplicates** are rarely legitimate in observation-level data — check *which* columns define a unique record.
- **dtype is meaning:** numbers stored as text block math; dates stored as text block time analysis.
- Cleaning = a sequence of **check → decide → apply → verify** steps, each documented.

## 3. Detailed lecture notes

**Why cleaning?** Start with the punchline: in industry, cleaning routinely takes
60–80% of project time, and every downstream step (EDA, models, AI tools) quietly
assumes clean input. A model trained on data with 30% missing values in one
column isn't "wrong" — it's silently learning a distorted pattern. Cleaning is
where you earn trust in your numbers.

**Missing values.** `NaN` is Pandas' marker. Detect: `df.isna()` → DataFrame of
True/False; `.sum()` per column; `.any(axis=1)` for rows with any missing. But
the key lesson is *why* data is missing: **Missing Completely At Random** (a
sensor dropped a reading — safe to drop or fill with mean), **Missing At Random**
(missingness relates to other columns you have — fill using those), and
**Missing Not At Random** (missingness is itself information — e.g., "salary left
blank by the highest earners"; dropping would bias you!). The remedy: don't
default to `dropna()`; think about the mechanism, then choose.

**Drop vs. fill.** `df.dropna()` drops any row with a missing value — costly on
wide tables. `df.dropna(subset=["critical_col"])` only drops when *that* column
is missing — usually the right call. Filling: `df.fillna(0)` (means "missing =
no value" — right for counts, wrong for temperature!), `df.fillna(df["col"].mean())`
(a crude but common imputation — state the caveat), `method="ffill"` for time
series (carry last known value forward). Always state what you did and why —
graders and colleagues need that markdown sentence.

**Duplicates.** `df.duplicated()` marks rows identical to an earlier row;
`.sum()` counts them. `df.drop_duplicates()` removes them. Critical question:
are *all* columns the identity of a record, or only some? Two patients with the
same name but different IDs aren't duplicates. Use
`df.drop_duplicates(subset=["patient_id"])` when that column defines uniqueness.
Keep `keep="first"`/`"last"` in mind.

**Wrong types.** `df.dtypes` reveals the damage: `object` column of numbers,
`object` column of dates. Fix: `df["col"].astype(float)` (will fail loudly on a
stray "N/A" — that's good: it surfaces dirty values for cleaning first),
`pd.to_datetime(df["date"])` for dates, `astype("category")` for small
categorical columns (memory + speed). Rule: **clean values first, then cast**
— casting before cleaning produces confusing errors.

**The cleaning loop.** For each column: (1) look — `info()`, `isna().sum()`,
`value_counts().head()`, `describe()`; (2) decide the fix based on the *why*;
(3) apply; (4) verify — re-run `info()`/`isna().sum()` and confirm. Document
each step in markdown. This loop is Lab 2 and Assignment 1 in miniature.

## 4. Important terminology

- **NaN / NA** — missing value marker.
- **`isna()` / `isnull()`** — detect missing; `notna()` detects present.
- **`dropna`** — remove rows/columns with missing values.
- **`fillna`** — replace missing values with a value or method.
- **Imputation** — filling missing values with estimates (mean, median, forward-fill).
- **MCAR / MAR / MNAR** — the three missing-data mechanisms (see notes above).
- **`duplicated` / `drop_duplicates`** — find / remove duplicate rows.
- **`astype`** — convert column dtype.
- **`to_datetime`** — parse a column into datetime type.
- **`describe()`** — summary statistics of numeric columns (count, mean, std, min, quartiles, max).

## 5. Python examples

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "name":  ["Ali", "Sara", "Usman", "Ali", None],
    "score": [82, None, 68, 82, 91],
    "date":  ["2024-01-05", "2024-01-06", "2024-01-07", "2024-01-05", "2024-01-08"],
})

# 1. Look
print(df.isna().sum())            # missing per column
print(df.duplicated().sum())      # duplicate rows

# 2. Decide
#    - "score" is missing once; drop only rows missing score
df = df.dropna(subset=["score"])
#    - duplicate rows defined by ALL columns -> drop them
df = df.drop_duplicates()
#    - fill remaining missing names with "unknown" (not ideal, but explicit)
df["name"] = df["name"].fillna("unknown")

# 3. Fix types
df["score"] = df["score"].astype(int)
df["date"] = pd.to_datetime(df["date"])

# 4. Verify
print(df.info())
```

## 6. Beginner example

```python
import pandas as pd

scores = pd.Series([85, None, 90, 76])
print(scores.isna().sum())       # 1 missing
print(scores.fillna(scores.mean()).round(1))   # 85.0 83.7 90.0 76.0
```

One missing value, two verbs: detect, then fill. Everything else today is
variations on this shape.

## 7. Practical Data Science example

```python
import pandas as pd
import seaborn as sns

# Penguins has documented missing values — a perfect practice dataset
df = sns.load_dataset("penguins")

# 1. Look
print(df.info())                        # 344 rows; note non-null counts
print(df.isna().sum())                  # 11 missing in culmen/bill cols, 2 in sex

# 2. Think about the mechanism
#    Missing bill measurements are usually measurement failures (safe to drop
#    or impute); missing sex is "could not determine" — still informative.

# 3. Decide & apply
#    Keep rows where the *key* columns are complete
df_clean = df.dropna(subset=["species", "bill_length_mm"])
#    Fill remaining numeric gaps with the species-group median (grouped imputation)
df_clean["bill_depth_mm"] = df_clean.groupby("species")["bill_depth_mm"].transform(
    lambda s: s.fillna(s.median())
)

# 4. Verify
print(df_clean.isna().sum())
```

## 8. In-class activity (50 min)

In `notebooks/week-05/session-09-cleaning-1.ipynb`:

1. **Inspect a messy frame (15 min):** load `penguins`; write a 5-row "dirty
   dataset" by hand (mix of missing values, one duplicate, one `object` column of
   numbers). Print `info()`, `isna().sum()`, `duplicated().sum()`.
2. **Missing-value decisions (15 min):** for three columns, write one sentence
   each: what kind of missingness, and drop or fill? Justify. Then apply.
3. **Duplicate drill (10 min):** create a frame with a row duplicated twice;
   drop duplicates; verify the count changed.
4. **Type fixes (10 min):** parse a `date` column with `to_datetime` and convert
   a text column of numbers with `astype(float)`.

## 9. Lab exercise

**Lab 09** (`labs/lab-09-data-cleaning-1.md`) — due before Session 10: data
cleaning I — missing values, duplicates, dtype conversion: detect, decide,
drop/fill, dedupe, fix types, verify. Submit via Git.

## 10. Common mistakes

- `dropna()` with no thought → deletes 40% of the data when only one column is the culprit.
- Filling everything with 0 or the mean without asking *why* it's missing.
- Checking duplicates without a `subset` when a partial key defines uniqueness.
- `astype(int)` on a column containing "N/A" → crash. Clean first, then cast.
- Ignoring `df.isna().sum()` after cleaning — always verify.
- Believing `describe()` output on a column that's secretly `object` (no statistics are computed — check dtypes first).
- Handling missing values *differently for train and test* — a preview of a modeling error (Sessions 17–22) — keep one cleaning function.

## 11. Short assessment questions

1. Which is better when 3 of 1000 rows have a missing value in a key column: `dropna()` or `fillna(0)`? Why?
2. What does `df.isna().sum()` tell you?
3. A salary column is missing for exactly the highest earners. Is dropping those rows safe? Why not?
4. What is the difference between `df.duplicated()` and `df.drop_duplicates(subset=["id"])`?
5. Your `age` column shows dtype `object` and `describe()` gives no statistics. What are two possible reasons, and what do you check first?
6. True/False: after cleaning, re-running `isna().sum()` is a waste of time. (False — verification is part of the loop.)

## 12. CLO mapping

CLO-1: cleaning is the "clean" verb in CLO-1 and the foundation of Assignment 1
and the EDA case study. The decide-before-apply habit also seeds the
documentation discipline that CLO-3 requires for AI-assisted steps.

## 13. Suggested homework

- Finish Lab 2 and push before Session 10.
- Practice: take `penguins` and clean it a second time with *different* choices
  (e.g., dropna all vs. median-fill); compare row counts and means. Write one
  paragraph: which choice was defensible and why?
- Read: pandas docs — "Working with missing data" (first three sections).
- Preview: run `df["name"].str.upper()` on a string column — Session 10 shows the `str` accessor, `apply`, and reshaping.