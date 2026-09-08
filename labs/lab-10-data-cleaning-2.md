# Lab 10 — Data Cleaning II: Strings, Dates, Outliers

**Session:** Week 5 · Session 10 · 90 min
**CLO:** CLO-1
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Clean text columns with `.str` methods (`strip`, `lower`, `contains`).
2. Parse dates with `pd.to_datetime` and extract components.
3. Detect outliers with the IQR rule and justify each removal.
4. Use `apply` and `map` for column-wise transforms.

## Problem statement

An events log is a mess: mixed-case venue names, a date column stored as
several formats, and a `duration_min` column with two impossible outliers
(typos). You must normalize text, unify dates, flag outliers, and produce a
tidy frame — with every decision logged.

## Dataset requirements

Built inline (30 rows, hand-made). No files.

## Step-by-step tasks

1. **Build** `events` from the starter code. Print `info()` and show that
   `date` is currently `object`.
2. **Text:** normalize `venue` with `.str.strip().str.title()`, and add a
   boolean column `is_online = venue.str.contains("Online")`. How many
   events are online?
3. **Dates:** convert `date` with `pd.to_datetime(events["date"], format=
   "mixed")`. Print the new dtype, then add columns `year`, `month`,
   `weekday` (via `.dt`).
4. **Outliers:** for `duration_min`, compute Q1, Q3, IQR. Flag rows outside
   `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]` as `is_outlier`. Print them; both must be
   the typo rows (≥ 700 min).
5. **Remove** outliers and confirm `describe()` for `duration_min` now looks
   sane (max well under 700).
6. **Map:** replace `type` codes (`"W" -> "Workshop"`, `"L" -> "Lecture"`,
   `"H" -> "Hackathon"`) using `.map()` with a dict.
7. **Apply:** add `attendance_rate = df.apply(lambda row: row["attendees"] /
   row["capacity"], axis=1)` rounded to 3, and comment on when `apply` is
   the right tool vs. plain column arithmetic.

## Starter code

```python
import pandas as pd
import numpy as np

events = pd.DataFrame({
    "title":     ["Intro to Git", "Pandas deep dive", "Kaggle 101",
                  "Docker basics", "SQL bootcamp", "ML workshop",
                  "Design sprint", "Data viz", "Web scraping", "AI talk",
                  "NumPy tricks", "GitHub Actions", "Regex hour", "APIs 101",
                  "Streamlit", "ETL patterns", "Cloud intro", "Testing py",
                  "Airflow", "Plotly", "FastAPI", "Polars", "BigQuery",
                  "dbt", "DuckDB", "Rust for data", "Excel tips",
                  "Jupyter magics", "CI/CD", "Notebooks at scale"] * 1,
    "venue":     ["Auditorium", "Online Zoom", "lab-2", "Auditorium",
                  "Online Zoom", "hall-1", "Studio", "lab-2", "Online zoom",
                  "Auditorium", "lab-1", "Online Zoom", "lab-1", "hall-2",
                  "Studio", "lab-2", "Auditorium", "lab-1", "Online Zoom",
                  "studio", "hall-1", "lab-2", "Auditorium", "Online Zoom",
                  "lab-1", "hall-2", "lab-2", "Studio", "Online zoom", "lab-1"],
    "date":      ["2024-01-05", "2024/01/12", "2024-01-19", "2024/01/26",
                  "2024-02-02", "2024/02/09", "2024-02-16", "2024/02/23",
                  "2024-03-01", "2024/03/08", "2024-03-15", "2024/03/22",
                  "2024-03-29", "2024-04-05", "2024/04/12", "2024-04-19",
                  "2024-04-26", "2024-05-03", "2024/05/10", "2024-05-17",
                  "2024-05-24", "2024/05/31", "2024-06-07", "2024/06/14",
                  "2024-06-21", "2024/06/28", "2024-07-05", "2024/07/12",
                  "2024-07-19", "2024/07/26"],
    "duration_min": [90, 60, 120, 90, 180, 720, 60, 90, 120, 45,
                     60, 90, 60, 120, 90, 60, 180, 90, 60, 120,
                     90, 60, 180, 90, 60, 120, 45, 90, 60, 1500],
    "type":      ["W", "L", "H", "W", "L", "W", "H", "L", "W", "L"] * 3,
    "attendees": [40, 120, 55, 38, 70, 60, 25, 90, 45, 130] * 3,
    "capacity":  [50, 200, 60, 50, 100, 80, 30, 100, 50, 150] * 3,
})

print(events.info())
# your code here
```

## Expected output

- `date` becomes `datetime64[ns]`; `year`, `month`, `weekday` columns exist.
- `is_online` True for 8 rows (note: `"Online zoom"` lowercase must be
  caught — that is the point of normalizing first).
- Outlier flag marks exactly the 720 and 1500 rows; after removal the max
  `duration_min` is 180.
- `type` shows `Workshop`, `Lecture`, `Hackathon` in `value_counts()`.
- `attendance_rate` between 0 and 1, rounded to 3.

## Questions

1. Why normalize `venue` **before** checking `contains("Online")`?
2. `format="mixed"` — what problem does it solve, and what is the safer
   alternative for real pipelines?
3. The IQR rule flagged 720 as an outlier. Would you always delete an
   outlier? Give one case where you would keep it.
4. `.map(dict)` vs `.apply(fn)` — when would you prefer `apply`?
5. What happens to a datetime column if one cell is `"not-a-date"`?

## Challenge task

Add a `weekend` boolean column using `.dt.dayofweek.isin([5, 6])`. Then
compute the mean attendance rate **per weekday name** (groupby on the
string weekday, not the number), sorted descending, and print the top 2.
Comment on why grouping by name instead of number can change the sort
order.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Text normalization + is_online | 4 | catches mixed case, 8 rows |
| Date parsing + components | 4 | dtype + 3 new columns |
| IQR outlier detection | 4 | flags exactly 720 & 1500 |
| Outlier removal + describe | 3 | max 180 after |
| `map` type expansion | 2 | full names in value_counts |
| `apply` attendance_rate | 3 | correct values, comment |
| Answers to questions | 2 | Q1, Q3 correct |
| Challenge: weekend + weekday means | 4 | top-2 + comment |
| **Total** | **26** | |