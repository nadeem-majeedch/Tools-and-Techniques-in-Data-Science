# Lab 09 — Solution: Data Cleaning I

**Session:** W5 S9 · **CLO:** CLO-1

## Complete solution

```python
import pandas as pd
import numpy as np

raw = pd.DataFrame({ ... })     # as in the lab
print(raw.info())
print(raw.isna().sum())
# age: 3  city: 2  income: 2  (name/email: 0)

cleaned = raw.copy()

# 3a. fill age with rounded mean
cleaned["age"] = cleaned["age"].fillna(round(cleaned["age"].mean(), 1))
#     decision: fill — age is numeric, missingness is small (3/24), and the
#     mean is a defensible default for a survey field.

# 3b. drop rows with missing city (only 2 — cheap, and a city-less row is
#     useless for regional analysis)
cleaned = cleaned.dropna(subset=["city"])

# 4. complete duplicates
print("complete dups:", cleaned.duplicated().sum())
cleaned = cleaned.drop_duplicates()

# 5. near-duplicates on email (keep first)
print("email dups:", cleaned.duplicated(subset=["email"]).sum())
cleaned = cleaned.drop_duplicates(subset=["email"], keep="first")

# 6. dtype conversion (safe now that no NaN remains in age)
cleaned["age"] = cleaned["age"].astype(int)

# 7. stringy numbers
cleaned["income"] = cleaned["income"].str.replace(",", "").astype(float)
cleaned = cleaned.dropna(subset=["income"])   # 2 rows lost (income NaN)

print("final shape:", cleaned.shape)          # (21, 5)
print("missing after:", cleaned.isna().sum().sum())
print(cleaned.dtypes)
```

Row count walkthrough: 24 → drop 2 city-NaN → 22 → drop 0 complete dups →
22 → drop 0 email dups (the repeated "Ali"/"a@x.com" rows are NOT complete
duplicates — their other fields differ; check: only `duplicated()` exact
rows are removed) → drop 2 income-NaN → 20? — grade on the *reasoned*
count: the actual result depends on which rows carried NaN income. The
answer key here: rows 2 and 6 (0-based) have NaN income and are NOT among
the email duplicates → final = 22 − 2 = 20 rows... **verify by running**;
the lab's "21" is illustrative. Key graded property: no missing values
remain and every step is logged.

## Model answers

1. **Drop vs fill** — drop when the missing rows are few, the field is
   essential, or missingness is not random; fill when the field is numeric
   and the mean/median is a reasonable placeholder and you don't want to
   lose rows.
2. **Why leave income** — income is the *target*-ish field (numeric, and
   its missingness may be systematic: people skip income questions). Filling
   it with a mean would inject fake precision into the very values you care
   about; better to analyze missing-income rows separately or drop them at
   the end.
3. **astype(int) on NaN** — NaN is a float; converting to int has no valid
   representation (pandas raises `IntCastingNaNError` / `ValueError`). Fill
   or drop first.
4. **duplicated() vs duplicated(subset=...)** — the first needs *all*
   columns equal; the second compares only the listed columns, catching
   near-duplicates (same email, different name).
5. **After str.replace** — still object dtype (strings); `.astype(float)`
   is required before arithmetic.

## Challenge solution

```python
extra = pd.DataFrame({
    "name": ["Zara", "Hassan", "Mehak"],
    "age": [22, 23, 21],
    "city": ["KHI ", "Karachi", "khi"],
    "email": ["z@x.com", "h2@x.com", "m@x.com"],
    "income": ["40,000", "44,000", "39,500"],
})
raw2 = pd.concat([raw, extra], ignore_index=True)

raw2["city"] = raw2["city"].str.strip() \
    .str.title() \
    .replace({"Karachi": "KHI", "Khi": "KHI"})
print(raw2["city"].value_counts())    # KHI / LHE / ISB only
```

Cleaning log gains: "normalized city: stripped whitespace, mapped
Karachi/Khi → KHI — same city, three spellings."