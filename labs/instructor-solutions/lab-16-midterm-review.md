# Lab 16 — Solution: Midterm Review

**Session:** W8 S16 · **CLO:** CLO-1

## Complete solution

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

flights = sns.load_dataset("flights")

# 1. load & shape
print(flights.shape)            # (144, 3)
print(flights.info())           # no nulls
print(flights.head())

# 2. clean month
flights["month"] = flights["month"].str.strip().str.capitalize()
print(flights["month"].value_counts())      # 12 months, title case

# 3. numpy stats
p = flights["passengers"]
print("mean", round(p.mean(), 1), "std", round(p.std(), 1))
print("min", p.min(), "max", p.max())
print("p25/p75:", np.percentile(p, [25, 75]).round(1))

# 4. aggregations
print("busiest year:", flights.groupby("year")["passengers"].sum().idxmax())
print("busiest month-row:", flights["passengers"].idxmax())
print(flights.loc[flights["passengers"].idxmax()])    # July 1960, 622

# 5. filter + sort
print(flights.nlargest(5, "passengers"))
big = flights[flights["passengers"] > 500]
print("rows > 500:", len(big))              # 8

# 6. plot (time axis via year + month)
flights["date"] = pd.to_datetime(
    flights["year"].astype(str) + "-" + flights["month"], format="%Y-%B")
plt.figure(figsize=(11, 4))
plt.plot(flights["date"], flights["passengers"])
plt.xlabel("Date"); plt.ylabel("Passengers")
plt.title("Monthly passengers 1949-1960")
plt.tight_layout()
plt.savefig("datasets/flights-trend.png", dpi=150, bbox_inches="tight")

# 7. written answers — see below
# 8. Restart & Run All — no errors
# 9. self-check against expected outputs
```

## Expected output

- min 104 (April 1949), max 622 (July 1960), mean ≈ 280.3, std ≈ 119.0.
- Busiest year 1960; busiest row July 1960.
- Rows > 500: 8.

## Model answers (task 7)

a. **Fastest growth: 1958–1960** — the line's slope steepens sharply in
   the last two years; e.g., 1958 total ≈ 28,400 vs 1960 ≈ 41,000 (roughly
   +45% in two years vs. earlier years' single digits).
b. **Normalize month before grouping** — the file's months may differ in
   case/spacing ("July" vs "july"), which would split one logical month
   into several groups and corrupt counts.
c. **Out-of-order months mislead** — a line plot connects points in row
   order; if months aren't chronological, the line zigzags and the "trend"
   is a visual artifact.

## Model answers (questions)

1. `.capitalize()` lowercases the rest ("jULY" → "July" is wrong-ish);
   leading spaces make `" July"` a distinct value. `strip()` first, then
   capitalize/title.
2. `idxmax()` on `groupby("year")["passengers"].sum()` returns the index
   label of the max — the year `1960`.
3. **Line over bar for time series** — a line encodes order and
   continuity (trend, slope, seasonality); bars imply discrete independent
   categories and hide the sequence.
4. `np.percentile(p, [25, 75])` returns an array of **two** numbers (a
   25th and a 75th percentile).
5. **KeyError 'month'** — (1) the DataFrame was overwritten by another
   cell (e.g., `flights = something_else`); (2) the column was renamed or
   the file re-read with different headers. Check the variable's current
   `columns` first.

## Challenge solution

```python
pivot = flights.pivot(index="year", columns="month", values="passengers")
print(pivot.loc[1960, "September"])
# pivot (not pivot_table): each (year, month) cell appears exactly once, so
# no aggregation is needed — pivot is the correct, simpler tool.
```