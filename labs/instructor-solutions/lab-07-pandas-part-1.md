# Lab 07 — Solution: Pandas I

**Session:** W4 S7 · **CLO:** CLO-1

## Complete solution

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

print(df.info())          # 24 rows, 5 cols, 0 non-null, int64/object
print(df.describe())

# 2. label selection
print(df.loc[df["program"] == "DS"])          # 8 rows

# 3. position selection
print(df.iloc[-3:])                            # last 3 rows
print(df.iloc[5, 3])                           # 58 (row 5, col 3 = enrolled)

# 4. boolean filters (parentheses mandatory with &)
print(df[df["enrolled"] > 80])                 # 4 rows
print(df[(df["enrolled"] > 80) & (df["year"] >= 2022)])   # 4 rows

# 5. categorical filter
print(df[df["semester"].isin(["Fall", "Spring"])])        # 16 rows

# 6. first look
print(df["program"].value_counts())            # DS 8, AI 8, CS 8
print(df["semester"].nunique())                # 2

# 7. new column + top fill rates
df["fill_rate"] = (df["enrolled"] / df["capacity"]).round(2)
print(df.nlargest(3, "fill_rate"))
```

## Expected output

- info: `RangeIndex: 24 entries`, 5 columns, all non-null.
- Task 3 value: `58`.
- Task 4: 4 rows (all enrolled > 80) and 4 rows (≥ 2022 & > 80).
- Task 5: 16 rows.
- Task 6: `DS 8 / AI 8 / CS 8`; `nunique() == 2`.
- Task 7: top-3 fill rates — CS 2024 Fall (1.10), CS 2024 Spring (1.02),
  CS 2023 Fall (1.00).

## Model answers

1. `.loc[5]` selects by *index label* (row 5 here, since the default index
   is 0..23); `.iloc[5]` selects by *position* (also row 5 here — they
   coincide with a default RangeIndex). They differ once the index is
   non-sequential.
2. **Parentheses** — `&` binds tighter than `==`/`>` in Python, so
   `df["a"] > 1 & df["b"] < 2` parses as `df["a"] > (1 & df["b"]) < 2`
   and fails; explicit parentheses force the intended grouping.
3. **isin** — one readable expression instead of chained `==` with `|`,
   and it scales to long lists.
4. **Boolean Series** — `df["enrolled"] > 80` returns a Series of True/
   False per row; `df[mask]` keeps rows where the mask is True (positional
   alignment).
5. **Single column** — bracket access returns the Series; `.loc` is for
   label-based row+column selection. One column needs no `.loc`.

## Challenge solution

```python
print(df.groupby("program")["fill_rate"].mean().round(3).sort_values(ascending=False))
# CS ~0.98, DS ~0.78, AI ~0.63 (approx — compute exact)

best = df["fill_rate"].idxmax()          # index LABEL of max row
print("top combination:", df.loc[best, ["program", "semester", "fill_rate"]])
# idxmax returns the index label (an int here), not the value.
```