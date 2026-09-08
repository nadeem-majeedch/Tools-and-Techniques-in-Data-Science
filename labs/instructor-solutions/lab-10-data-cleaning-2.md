# Lab 10 — Solution: Data Cleaning II

**Session:** W5 S10 · **CLO:** CLO-1

## Complete solution

```python
import pandas as pd
import numpy as np

events = pd.DataFrame({ ... })     # as in the lab

# 2. text normalization
events["venue"] = events["venue"].str.strip().str.title()
events["is_online"] = events["venue"].str.contains("Online")
print("online events:", events["is_online"].sum())     # 8

# 3. dates
events["date"] = pd.to_datetime(events["date"], format="mixed")
print("dtype:", events["date"].dtype)                  # datetime64[ns]
events["year"] = events["date"].dt.year
events["month"] = events["date"].dt.month
events["weekday"] = events["date"].dt.day_name()

# 4. IQR outliers on duration_min
q1, q3 = events["duration_min"].quantile([0.25, 0.75])
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
events["is_outlier"] = (events["duration_min"] < lo) | (events["duration_min"] > hi)
print(events.loc[events["is_outlier"], "duration_min"])  # 720 and 1500

# 5. remove
events = events[~events["is_outlier"]]
print(events["duration_min"].describe()["max"])          # 180

# 6. map type codes
events["type"] = events["type"].map({"W": "Workshop", "L": "Lecture",
                                     "H": "Hackathon"})
print(events["type"].value_counts())

# 7. apply for row-wise ratio
events["attendance_rate"] = events.apply(
    lambda row: row["attendees"] / row["capacity"], axis=1).round(3)
print(events["attendance_rate"].describe())
```

## Expected output

- 8 online events (catches lowercase "Online zoom" — that's why we
  normalize first).
- date dtype datetime64; year/month/weekday columns populated.
- Outliers: exactly 720 and 1500; max after removal: 180.
- `type`: Workshop 8, Lecture 8, Hackathon 6 (or per data).
- attendance_rate ∈ [0, 1].

## Model answers

1. **Normalize first** — `.str.contains("Online")` is case-sensitive by
   default; "Online zoom" would be missed. `strip().title()` unifies
   casing/whitespace so the pattern match is reliable.
2. **format="mixed"** — the column contains both `2024-01-05` and
   `2024/01/12` styles; `format="mixed"` lets pandas infer each; the safer
   production alternative is to standardize at the source or use
   `dayfirst`/explicit formats per source.
3. **Keep an outlier?** — yes: if it's a real measurement (e.g., a
   12-hour hackathon), if the domain says extreme values are legitimate, or
   if the analysis is robust (median-based). Outlier removal should be
   justified, not automatic.
4. **map vs apply** — `map(dict)` is ideal for lookup/replacement by
   category; `apply(fn, axis=1)` is for row-wise computations involving
   multiple columns (like a ratio).
5. **Bad date cell** — `pd.to_datetime(..., format="mixed")` raises
   (or errors= parameter controls it); the whole column conversion fails
   rather than silently producing NaT — a feature, since you can then
   locate the bad cell.

## Challenge solution

```python
events["weekend"] = events["date"].dt.dayofweek.isin([5, 6])
print(events["weekend"].value_counts())

top = (events.groupby("weekday")["attendance_rate"].mean()
       .sort_values(ascending=False))
print(top.head(2))
# Grouping by NAME sorts alphabetically by default in groupby output order
# (order of first appearance); sort_values re-sorts numerically — the point
# of the comment.
```